import contextlib
import functools
import gc
import inspect
import math
import random
import re
import string
import warnings
from typing import Callable, List, Optional, Tuple, Union

import numpy as np
import torch
from torch import Tensor
from torch._dynamo import config
from torch._dynamo.exc import TorchDynamoException
from torch.backends import cudnn, opt_einsum
from torch.utils._pytree import tree_map

config.cache_size_limit = 2**16

compile_mode = "max-autotune-no-cudagraphs"
dynamic = False
compile_mode_recommended_to_none = None
zeroth_power_mode = "qr"  # 'qr' is baseline, 'newtonschulz' converges better and faster
tiny_bf16 = torch.finfo(torch.bfloat16).tiny
_cudnn_double_backward_pattern = re.compile(
    r"the derivative for .* is not implemented\. Double backwards .* To run double backwards"
)
_torch_compile_double_backward_pattern = re.compile(r"compile.*does not currently support double backward")
_fd_error = (
    "You can accelerate startup by globally enabling finite_differences first "  #
    "(via opt.finite_differences=True or by subclassing it)\n"
    "Original Error: "
)


def decorator(func):
    compiled = None

    @functools.wraps(func)
    def _fn(*args, **kwargs):
        if is_compiling() or compile_mode_recommended_to_none is None:
            return func(*args, **kwargs)
        nonlocal compiled
        if compiled is None:
            compiled = torch.compile(fullgraph=True, dynamic=dynamic, mode=compile_mode_recommended_to_none)(func)
        return compiled(*args, **kwargs)

    return _fn


def decorator_knowngood(func: Callable):
    compiled = None

    @functools.wraps(func)
    def _fn(*args, **kwargs):
        if is_compiling() or compile_mode is None:
            return func(*args, **kwargs)
        nonlocal compiled
        if compiled is None:
            compiled = torch.compile(fullgraph=True, dynamic=dynamic, mode=compile_mode)(func)
        return compiled(*args, **kwargs)

    return _fn


einsum_base = string.ascii_lowercase


@decorator_knowngood
def _compilable_schedule_free_(
    p: List[Tensor],
    z: List[Tensor],
    ckp1: Tensor,
    update: List[Tensor],
    lr: Tensor,
    beta1: Tensor,
    decay: float,
    grad: List[Tensor],
    caution,
):
    for op, oz, u_, g_ in zip(p, z, update, grad):
        u_ = u_.view_as(op)
        p_, z_, u_ = map(promote, (op, oz, u_))
        if decay != 0:
            u_ = u_ + p_ * decay
        if caution:
            u_ = _compilable_cautioning(u_, g_)
        p_ = p_.lerp(z_, ckp1)
        p_ = p_ + u_ * (lr * (beta1 * (1 - ckp1)) - lr)
        z_ = z_ + u_ * -lr
        copy_stochastic_(op, p_)
        copy_stochastic_(oz, z_)


def schedule_free_(
    lr: float,
    weight_lr_power: float,
    weight_sum: float,
    beta1: float,
    parameters: List[Tensor],
    z: List[Tensor],
    update: List[Tensor],
    grad: List[Tensor],
    caution: bool = False,
    r: float = 0.0,
    step: int = 0,
    decay: float = 0.0,
):
    weight = abs(lr) ** weight_lr_power * max(step, 1) ** r
    weight_sum = weight_sum + weight

    try:
        ckp1 = weight / weight_sum
    except ZeroDivisionError:
        ckp1 = 0

    update, parameters, z, grad = list_guard(update, parameters, z, grad)
    lr, ckp1, beta1 = scalar_guard(lr, ckp1, beta1, grad[0])
    _compilable_schedule_free_(parameters, z, ckp1, update, lr, beta1, decay, grad, caution)
    return weight_sum


def append_or_extend(base, new):
    if isinstance(new, list):
        base.extend(new)
    else:
        base.append(new)


def dim_merger(grad, max_precond_dim, split: bool = False):
    """
    Merges dimensions of the gradient tensor till the product of the dimensions is less than or equal to max_precond_dim.

    we don't want to merge fan-in into fan-out,
    but we want to merge conv kernels into fan-in or at least merge the kernel
    so, [128, 64, 3, 3] should result in [128, 576] or [128, 64, 9] instead of [73728] or [8192, 3, 3] the baseline
    would've done

    By @francois-rozet (commit: 68cde41eaf7e73b4c46eacb6a944865dcc081f1d), re-commited due to faulty merge
    """
    new_shape = []
    cum_size = 1

    for s in grad.shape[1:][::-1]:
        temp_size = cum_size * s
        if temp_size > max_precond_dim:
            if cum_size > 1:
                new_shape.append(cum_size)
                cum_size = s
            else:
                new_shape.append(s)
                cum_size = 1
        else:
            cum_size = temp_size

    if cum_size > 1:
        new_shape.append(cum_size)

    new_shape = [grad.shape[0], *new_shape[::-1]]
    new_grad = grad.reshape(new_shape)
    if not split:
        return new_grad

    grads = [new_grad]
    for i, sh in reversed(list(enumerate(new_shape[:]))):
        if sh == 1:
            grads = [g.squeeze(dim=i) for g in grads]
            continue
        if sh <= max_precond_dim:
            continue
        grads = [a for g in grads for a in g.split(max_precond_dim, dim=i)]
    if len(grads) == 1:
        return new_grad
    new_grads = []
    for g in grads:
        append_or_extend(new_grads, dim_merger(g, max_precond_dim, split))
    return new_grads


def beta_debias(beta, step):
    return 1 - (1 - beta) / (1 - beta**step)


def eps_sqrt(item, eps):
    return item.sqrt().clamp(min=eps)


@decorator_knowngood
def _compilable_exp_avg_sq_(
    state: List[Tensor], grad: List[Tensor], beta2: Tensor, eps: Tensor, out: List[Optional[Tensor]]
):
    g32 = promote(grad)
    s32 = _lerp(state, torch._foreach_mul(g32, g32), beta2)

    denom = [eps_sqrt(d, eps) for d in s32]

    if out[0] is None:
        return denom

    copy_stochastic_list_(out, denom)
    return out


def exp_avg_sq_(state, grad, beta2, eps, out=None):
    state, grad, out = list_guard(state, grad, out)
    beta2, eps = scalar_guard(beta2, eps, state[0])
    return _compilable_exp_avg_sq_(state, grad, beta2, eps, out)


@decorator_knowngood
def _compilable_scale_by_exp_avg_sq_(state: List[Tensor], grad: List[Tensor], beta2: Tensor, eps: Tensor):
    g32 = promote(grad)
    denom = _compilable_exp_avg_sq_(state, g32, beta2, eps, [None])
    out = torch._foreach_div(g32, denom)
    copy_stochastic_list_(grad, out)


def scale_by_exp_avg_sq_(exp_avg_sq, grad, beta2, eps):
    grad, exp_avg_sq = list_guard(grad, exp_avg_sq)
    beta2, eps = scalar_guard(beta2, eps, grad[0])
    _compilable_scale_by_exp_avg_sq_(exp_avg_sq, grad, beta2, eps)
    return grad


@decorator_knowngood
def _compilable_exp_avg_(state, grad, beta):
    lerped = _lerp(state, grad, beta)
    copy_stochastic_list_(grad, lerped)


def scale_by_exp_avg_(state, grad, beta):
    state, grad = list_guard(state, grad)
    beta = scalar_guard(beta, state[0])
    _compilable_exp_avg_(state, grad, beta)
    return grad


@decorator_knowngood
def _compilable_agc_(parameters: List[Tensor], gradients: List[Tensor], clip_val: float, minimum: float, eps: float):
    p32, g32 = [list(map(promote, x)) for x in (parameters, gradients)]
    p_norm = torch._foreach_norm(p32)
    g_norm = torch._foreach_norm(g32)
    p_norm = torch._foreach_maximum(p_norm, minimum)
    g_norm = torch._foreach_maximum(g_norm, eps)
    p_norm = torch._foreach_div(p_norm, g_norm)
    p_norm = torch._foreach_mul(p_norm, clip_val)
    p_norm = torch._foreach_minimum(p_norm, 1)
    g32 = torch._foreach_mul(g32, p_norm)
    copy_stochastic_list_(gradients, g32)


def adaptive_gradient_clipping_(
    parameters: List[Tensor], gradients: List[Tensor], clip_val: float, minimum: float = 1e-3, eps: float = 1e-8
):
    if clip_val <= 0:
        return gradients
    parameters, gradients = list_guard(parameters, gradients)
    clip_val = scalar_guard(clip_val, parameters[0])
    _compilable_agc_(parameters, gradients, clip_val, minimum, eps)
    return gradients


def is_compiling():
    try:
        return torch.compiler.is_compiling()
    except TorchDynamoException:
        return True


def set_(dst: Tensor, src: Tensor):
    dst.copy_(src)


def clean():
    torch.cuda.empty_cache()
    gc.collect()


def _ignore_warning(msg):
    warnings.filterwarnings("ignore", f".*{msg}.*")


def set_torch(benchmark_limit: int = 32, einsum_strategy: str = "auto"):
    cudnn.benchmark = True
    cudnn.deterministic = False
    cudnn.benchmark_limit = benchmark_limit
    torch.use_deterministic_algorithms(False)
    torch.set_float32_matmul_precision("high")  # highest: FP32, high: TF32, medium: bf16
    opt_einsum.set_flags(True, einsum_strategy)

    # Torch calls these for 2nd-order optimization in HeavyBall, but they are explicitly handled.
    _ignore_warning(
        "Using backward() with create_graph=True will create a reference cycle between the parameter and its gradient which can cause a memory leak"
    )
    _ignore_warning(
        "We recommend using autograd.grad when creating the graph to avoid this. If you have to use this function, make sure to reset the .grad fields of your parameters to None after use to break the cycle and avoid the leak"
    )


@decorator
def zeropower_via_newtonschulz5(G, steps=5, eps=1e-7):
    assert len(G.shape) == 2
    a, b, c = (3.4445, -4.7750, 2.0315)
    X = G.to(torch.bfloat16 if G.dtype != torch.float64 else G.dtype)  # Preserve float64 if present
    X /= X.norm() + eps  # ensure top singular value <= 1
    if G.size(0) > G.size(1):
        X = X.T
    for _ in range(steps):
        A = X @ X.T
        B = b * A + c * A @ A  # adapted from suggestion by @jxbz, @leloykun, and @YouJiacheng
        X = a * X + B @ X
    if G.size(0) > G.size(1):
        X = X.T
    return X.to(G.dtype)


def ortho(x):
    if zeroth_power_mode == "qr":
        return torch.linalg.qr(x).Q
    if zeroth_power_mode == "svd":
        u, _s, v = torch.linalg.svd(x)
        return u @ v.T
    raise NotImplementedError(f"Unknown zeroth_power_mode: {zeroth_power_mode}")


@decorator_knowngood
def _compilable_heavyball_momentum_(state, grad, beta):
    s32, g32 = [list(map(promote, x)) for x in (state, grad)]
    s32 = torch._foreach_mul(s32, beta)
    s32 = torch._foreach_add(s32, g32)
    copy_stochastic_list_(state, s32)
    copy_stochastic_list_(grad, s32)


@decorator_knowngood
def _compilable_nesterov_momentum_(state, grad, beta):
    s32, g32 = [list(map(promote, x)) for x in (state, grad)]
    s32 = torch._foreach_mul(s32, beta)
    s32 = torch._foreach_add(s32, g32)
    g32 = [g + s * beta for g, s in zip(g32, s32)]
    copy_stochastic_list_(state, s32)
    copy_stochastic_list_(grad, g32)


def heavyball_momentum(state, grad, beta):
    state, grad = list_guard(state, grad)
    beta = scalar_guard(beta, state[0])
    _compilable_heavyball_momentum_(state, grad, beta)
    return grad


def nesterov_momentum(state, grad, beta):
    state, grad = list_guard(state, grad)
    beta = scalar_guard(beta, state[0])
    _compilable_nesterov_momentum_(state, grad, beta)
    return grad


@decorator_knowngood
def _compilable_nesterov_ema_(state, grad, beta):
    ema32 = _lerp(state, grad, beta)
    stochastic_add_(grad, ema32, 1)


def nesterov_ema(state, grad, beta):
    state, grad = list_guard(state, grad)
    beta = scalar_guard(beta, state[0])
    _compilable_nesterov_ema_(state, grad, beta)
    return grad


@decorator_knowngood
def _compilable_grafting(magnitude, direction):
    return direction * (magnitude.norm() / direction.norm().clamp(min=1e-6))


@decorator_knowngood
def inplace_orthogonal_(x: Tensor, mode: str, out: Tensor, scale_mode: str):
    if mode == "newtonschulz" or x.shape[0] != x.shape[1]:
        y = zeropower_via_newtonschulz5(x, 5)
    elif mode == "qr":
        y = torch.linalg.qr(promote(x)).Q
    elif mode == "svd":
        u, _s, v = torch.linalg.svd(promote(x))
        y = u @ v.T
    else:
        raise NotImplementedError(f"Unknown zeroth_power_mode: {mode}")
    if scale_mode == "none":
        pass
    elif scale_mode == "scale":
        y *= max(1, x.size(0) / x.size(1)) ** 0.5
    elif scale_mode == "graft":
        y = _compilable_grafting(x, y)
    else:
        raise NotImplementedError(f"Unknown scale_mode: {scale_mode}")
    set_(out, y)


@decorator_knowngood
def _compilable_scatter_set(target, source, index):
    target[:] = source.contiguous()[index].reshape_as(target)


# @decorator_knowngood
def get_orthogonal_matrix_QR(GG: List[Tensor], Q: List[Tensor], exp_avg: Optional[Tensor] = None):
    """
    Computes the eigenbases of the preconditioner using one round of power iteration
    followed by torch.linalg.qr decomposition, and updates exp_avg in-place from old to new eigenspace.

    :param GG: List of accumulated gradient outer products.
    :param Q: List of current eigenbases (updated in-place to Q_new).
    :param exp_avg: Exponential moving average in the old eigenspace (updated in-place if provided).
    """
    if isinstance(Q, list) and not Q:
        return

    if exp_avg is not None and exp_avg.dim() != len(Q):
        raise ValueError(f"exp_avg dim {exp_avg.dim()} does not match Q length {len(Q)}")

    new_qs = []

    for m, q in zip(GG, Q):
        if m is None:
            new_qs.append(None)
            continue

        m = promote(m.data)
        q_old = promote(q.data)

        tmp = m @ q_old
        est_eig = torch.einsum("ij,ij->j", q_old, tmp)
        sort_idx = torch.argsort(est_eig, descending=True)

        tmp[:, sort_idx], _ = torch.linalg.qr(tmp[:, sort_idx])
        new_qs.append(tmp)

    if exp_avg is None:
        for q, q_new in zip(Q, new_qs):
            copy_stochastic_(q, q_new)
        return

    assert exp_avg.ndim < 13, "exp_avg.ndim must be less than 13"
    in_str = einsum_base[: exp_avg.dim()]
    out_str = einsum_base[exp_avg.dim() : 2 * exp_avg.dim()]

    from_shampoo = ",".join([o + i for m, i, o in zip(Q, in_str, in_str.upper()) if m is not None])
    if not from_shampoo:
        return

    to_shampoo = ",".join([i + o for m, i, o in zip(new_qs, in_str.upper(), out_str) if m is not None])
    out_str = "".join([o if o in to_shampoo else i for i, o in zip(in_str, out_str)])

    subscripts = f"{in_str},{from_shampoo},{to_shampoo}->{out_str}"
    exp_avg_new = torch.einsum(
        subscripts, exp_avg, *[q for q in Q if q is not None], *[q for q in new_qs if q is not None]
    )
    copy_stochastic_(exp_avg, exp_avg_new)

    for q, q_new in zip(Q, new_qs):
        if q is not None:
            copy_stochastic_(q, q_new)


def get_orthogonal_matrix(mat, max_eps: float = 1e-3, min_eps: float = 1e-30):
    """
    Computes the eigenbases of the preconditioner using torch.linalg.eigh decomposition.
    """

    final = []
    for m in mat:
        if m is None:
            final.append(None)
            continue

        m = promote(m.data)

        device, dtype = m.device, m.dtype
        eps = min_eps
        while True:
            try:
                eye = torch.eye(m.shape[0], device=m.device, dtype=m.dtype)
                _eigval, eigvec = torch.linalg.eigh(m + eps * eye)
                eigvec = eigvec.to(device=device, dtype=dtype)
                break
            except torch.OutOfMemoryError:
                if m.device.type == "cpu":
                    raise
                else:
                    m = m.cpu()
            except RuntimeError:  # failed to compute eigenvalues
                if m.dtype != torch.double:
                    m = m.double()
                elif eps < max_eps:
                    eps = eps ** (2 / 3)
                else:
                    raise
            clean()

        eigvec = eigvec.to(device=m.device, dtype=m.dtype)
        eigvec = torch.flip(eigvec, [1])
        final.append(eigvec)

    return final


@decorator_knowngood
def _compilable_stochastic_lerp_(x: List[Tensor], y: List[Tensor], a: Union[float, int, Tensor]):
    for x_, y_ in zip(x, y):
        x32 = promote(x_)
        y32 = promote(y_)
        if x32.dtype != y32.dtype:
            y32 = y32.to(x32.dtype)
        copy_stochastic_(x_, x32 * (1 - a) + y32 * a)


def get_beta1(group):
    beta = None
    if "beta" in group:
        beta = group["beta"]
    if beta is None and "betas" in group:
        beta = group["betas"][0]
    if beta is None:
        raise ValueError("Beta not found in group.")
    return beta


def get_beta2(group):
    if "palm" in group and group["palm"] is True and "beta2_scale" in group:
        step = max(group.get("step", 1), 1)
        return 1 - step ** -group["beta2_scale"]
    if "betas" in group:
        return group["betas"][1]
    raise ValueError("Beta2 not found in group.")


def stochastic_lerp_(x: List[Tensor], y: List[Tensor], a: Union[float, int, Tensor]):
    x, y = list_guard(x, y)
    a = scalar_guard(a, x[0])
    _compilable_stochastic_lerp_(x, y, a)


def list_guard(*xs):
    out = []
    for x in xs:
        if isinstance(x, (list, tuple)):
            out.append(x)
        else:
            out.append([x])
    if len(xs) == 1:
        return out[0]
    return out


def scalar_guard(*args):
    *xs, ref = args
    out = []
    for x in xs:
        if isinstance(x, float):
            out.append(torch.empty((), dtype=promote(ref.dtype), device=ref.device).fill_(x))
        elif isinstance(x, int):
            out.append(torch.empty((), dtype=torch.int64, device=ref.device).fill_(x))
        else:
            out.append(x)
    if len(xs) == 1:
        return out[0]
    return out


@decorator_knowngood
def _compilable_stochastic_add_(x: List[Tensor], y: List[Tensor], alpha: Union[float, int, Tensor]):
    for x_, y_ in zip(x, y):
        x32 = promote(x_)
        y32 = promote(y_)
        copy_stochastic_(x_, x32 + y32 * alpha)


def stochastic_add_(x: List[Tensor], y: List[Tensor], alpha: Union[float, int, Tensor] = 1):
    x, y = list_guard(x, y)
    alpha = scalar_guard(alpha, x[0])
    _compilable_stochastic_add_(x, y, alpha)


@decorator_knowngood
def _compilable_stochastic_add_divide_(x: List[Tensor], y: List[Tensor], alpha: Tensor, divisor: Tensor):
    for x_, y_ in zip(x, y):
        x32 = promote(x_)
        y32 = promote(y_)
        copy_stochastic_(x_, (x32 + y32 * alpha) / divisor)


def stochastic_add_divide_(x: List[Tensor], y: List[Tensor], alpha: Union[float, int, Tensor] = 1, divisor: float = 1):
    x, y = list_guard(x, y)
    alpha, divisor = scalar_guard(alpha, divisor, x[0])
    _compilable_stochastic_add_divide_(x, y, alpha, divisor)


@decorator_knowngood
def _compilable_stochastic_multiply_(x: List[Tensor], y: List[Tensor]):
    for x_, y_ in zip(x, y):
        x32 = promote(x_)
        y32 = promote(y_)
        copy_stochastic_(x_, x32 * y32)


def stochastic_multiply_(x: List[Tensor], y: List[Tensor]):
    x, y = list_guard(x, y)
    _compilable_stochastic_multiply_(x, y)


@decorator
def update_ggt(grad, GG, max_precond_dim, precondition_1d, beta):
    """
    Simplified by @francois-rozet in commit 704ccc4bab52429f945df421647ec82c54cdd65f
    Re-commited due to faulty merge
    """
    if grad.dim() == 1 and (not precondition_1d or grad.shape[0] > max_precond_dim):
        return

    for idx, m in enumerate(GG):
        if not isinstance(m, Tensor):
            continue
        b = einsum_base[idx]
        g0 = einsum_base[: grad.dim()]
        g1 = g0.replace(b, b.upper())
        outer_product = torch.einsum(f"{g0},{g1}->{b + b.upper()}", grad, grad)
        stochastic_lerp_(m, outer_product, 1 - beta)


def tree_apply(fn):
    def _fn(*args):
        return tree_map(fn, *args)

    return _fn


@tree_apply
def promote(x):
    if isinstance(x, torch.dtype) and x in (torch.bfloat16, torch.float16):
        return torch.float32
    if isinstance(x, Tensor) and x.dtype in (torch.bfloat16, torch.float16):
        return x.float()
    return x


def promote_detach(x, should_promote):
    if x is None:
        return x
    if should_promote:
        x = promote(x)
    return x.detach()


def detach(x):
    if isinstance(x, Tensor):
        return x.detach()
    return x


def min_dtype(xs: List[Tensor]):
    dtypes = [x.dtype for x in xs]
    for d in (torch.float32, torch.bfloat16, torch.float16):
        if all(x in (d, torch.float32, torch.float64) for x in dtypes):
            return d
    return torch.float32


def update_preconditioner(grad, Q, GG, exp_avg, max_precond_dim, precondition_1d, beta, update_precond):
    """
    Updates the preconditioner matrices and the eigenbases (L, R, Q_L, Q_R in the paper).
    """
    update_ggt(grad, GG, max_precond_dim, precondition_1d, beta)
    if update_precond:
        get_orthogonal_matrix_QR(GG, Q, exp_avg)


def init_preconditioner(grad, state, max_precond_dim, precondition_1d):
    """
    Initializes the preconditioner matrices (L and R in the paper).
    """
    state["GG"] = []  # Will hold all the preconditioner matrices (L and R in the paper).
    if grad.numel() > 1 and (grad.ndim > 1 or precondition_1d):
        for sh in grad.shape:
            if sh > max_precond_dim or sh == 1:
                # via @francois-rozet: https://github.com/HomebrewML/HeavyBall/commit/8b86be04967e2d095136d5603724f488f2d46592#diff-a430393dd0a6ee393944a9ed16416115c175de2414cf4a96e647197697f265e9R621
                state["GG"].append(None)
            else:
                state["GG"].append(torch.zeros(sh, sh, device=grad.device, dtype=grad.dtype))
    else:
        state["GG"].append(None)

    update_ggt(grad, state["GG"], max_precond_dim, precondition_1d, 0)
    state["Q"] = get_orthogonal_matrix(state["GG"])


@decorator
def project(grad, Q, back: bool):
    """
    :param grad:
    :param Q:
    :param back: whether to project to Shampoo eigenbases or back to original space
    :return:
    """
    param = einsum_base[: grad.dim()]
    preconditioners = ",".join([(g + g.upper())[:: -1 if back else 1] for m, g in zip(Q, param) if m is not None])
    if preconditioners:
        out = "".join([c.upper() if c.upper() in preconditioners else c for c in param])
        out = torch.einsum(f"{param},{preconditioners}->{out}", promote(grad), *[q for q in Q if q is not None])
        grad = out.to(grad.dtype)
    return grad


@contextlib.contextmanager
def patch_backward():
    @contextlib.contextmanager
    def _inner(module):
        original = module.backward

        signature = inspect.signature(original)

        def patched_backward(*args, **kwargs):
            new_kwargs = signature.bind(*args)
            new_kwargs.apply_defaults()
            new_kwargs = new_kwargs.arguments
            new_kwargs.update(kwargs)
            new_kwargs["create_graph"] = True
            return original(**new_kwargs)

        module.backward = patched_backward
        yield
        module.backward = original

    with _inner(torch.Tensor), _inner(torch.autograd):
        yield


def hasattr_none(obj, name):
    return getattr(obj, name, None) is not None


class ExactHVPFailed(ValueError):
    pass


class StatefulOptimizer(torch.optim.Optimizer):
    """
    finite_differences saves memory, but needs more compute. (Alternative is true HVP)
    Both `True` and `False` have some edge cases they don't support, so experiment with it.
    The previous (heavyball<=1.5.3) default was `True`, which is incompatible with some benchmarks but works better with RevNet
    Further notice that both methods have different numerics outputs
    """

    ema_decay: float = 0.001
    compile_step: bool = False
    hessian_approx: bool = False
    precond_schedule: Union[Callable, float, None] = None
    stochastic_schedule: bool = False
    finite_differences: bool = False
    fallback_to_finite_differences: bool = True
    _fallback_enabled: bool = False
    hvp_interval: int = 1  # grad is faster initially, hvp later

    def __init__(self, params, defaults, foreach: bool = True, use_ema: bool = False):
        super().__init__(params, {**defaults, "foreach": foreach})
        self.use_ema = use_ema
        self.mapping = {}
        self._inner_group = {"stochastic_schedule": self.stochastic_schedule}
        self._precond_rng = random.Random(0x12312)
        self._is_preconditioning = None

        if self.hessian_approx and self.compile_step:
            raise ValueError("Hessian approximation can't be used with compile_step.")

    def get_groups(self, group):
        return [group]

    def state_(self, arg: Tensor):
        return self.state[arg]

    def mars_correct_list(self, group, p_list, g_list, mars_gamma, beta):
        for p, g in zip(p_list, g_list):
            state = self.state_(p)
            if "mars_old_grad" not in state:
                state["mars_old_grad"] = torch.zeros_like(g)
        old_gs = [self.state_(p)["mars_old_grad"] for p in p_list]
        mars_correction(g_list, old_gs, mars_gamma, beta)

    def split_p_and_g_in_group(
        self,
        group: dict,
        skip_none: bool = True,
        should_promote: bool = True,
        beta1: float = -1.0,
        raw: bool = False,
    ):
        for p in group["params"]:
            grad = getattr(p, "grad", None)
            if grad is None and skip_none:
                continue

            p.grad = None

            if raw:
                yield p, grad
                continue

            if p in self.mapping:
                p_views = self.mapping[p]
            else:
                self.mapping[p] = p_views = merge_group(group, p)

            vector = getattr(p, "vector", None)
            hessian_vector = getattr(p, "hessian_vector", None)
            p.vector = None
            p.hessian_vector = None

            grad, vs, hvs = [
                [None] * len(p_views) if x is None else merge_group(group, x)  #
                for x in (grad, vector, hessian_vector)
            ]

            for pv, g, v, hv in zip(p_views, grad, vs, hvs):
                g = promote_detach(g, should_promote)
                if beta1 >= 0 and group.get("mars", False):
                    self.mars_correct_list(group, [pv], [g], group["mars_gamma"], beta1)
                pv.vector = promote_detach(v, should_promote)
                pv.hessian_vector = promote_detach(hv, should_promote)
                yield pv, g

    def state_size(self) -> int:
        total_bytes = 0

        def _add(x):
            nonlocal total_bytes
            if isinstance(x, Tensor):
                total_bytes += x.numel() * x.element_size()

        for group in self.param_groups:
            for p, _ in self.split_p_and_g_in_group(group, skip_none=False):
                tree_map(_add, self.state_(p))
        return total_bytes

    def _step(self, group):
        raise NotImplementedError

    def ema_update(self):
        with torch.no_grad():
            for group in self.param_groups:
                active_p = [p for p in group["params"]]

                if not active_p:
                    return

                k = group["ema_step"] = group.get("ema_step", -1) + 1

                for p in active_p:
                    if "param_ema" not in self.state_(p):
                        self.state_(p)["param_ema"] = torch.zeros_like(p.data, memory_format=torch.preserve_format)

                y, param_ema = zip(*[(p.data, self.state_(p)["param_ema"]) for p in active_p])
                torch._foreach_lerp_(param_ema, y, weight=beta_debias(1 - self.ema_decay, k + 1))

    def copy_emas_to_params(self):
        with torch.no_grad():
            for group in self.param_groups:
                active_p = [p for p in group["params"]]

                if not active_p:
                    return

                for p in active_p:
                    if "param_ema" in self.state_(p):
                        p_clone = p.data.clone()
                        set_(p.data, self.state_(p)["param_ema"])
                        set_(self.state_(p)["param_ema"], p_clone)

    def copy_params_to_emas(self):
        with torch.no_grad():
            for group in self.param_groups:
                active_p = [p for p in group["params"]]

                if not active_p:
                    return

                for p in active_p:
                    if "param_ema" in self.state_(p):
                        ema_clone = self.state_(p)["param_ema"].data.clone()
                        set_(self.state_(p)["param_ema"], p.data)
                        set_(p.data, ema_clone)

    def _finite_differences_hvp(self, closure):
        with torch.enable_grad():
            loss = closure()  # closure without retain_graph=True

        grads = []
        for group in self.param_groups:
            for p, g in self.split_p_and_g_in_group(group, skip_none=True, raw=True):
                grads.append(g)
                p.vector = torch.randn_like(p)
                p.orig = p.data.clone()
                # scale taken from https://github.com/lixilinx/psgd_torch/blob/1943e66596111e78157ca1b72b31c1dfdf0653ef/preconditioned_stochastic_gradient_descent.py#L2161
                stochastic_add_(p.data, p.vector, torch.finfo(p.dtype).eps ** 0.5)

        with torch.enable_grad():
            closure()

        # we don't subtract the vector here again to avoid accumulating error from (x + eps - eps + eps - eps)
        # this costs more memory, but the imprecision seems too severe to use the other method
        for group in self.param_groups:
            for p, g in self.split_p_and_g_in_group(group, skip_none=True, raw=True):
                p.grad = grads.pop(0)
                stochastic_add_(g, p.grad, -1)  # technically, we have to divide by the scale here
                p.hessian_vector = g
                p.data.copy_(p.orig)
                del p.orig
        return loss

    def _double_backward_hvp(self, closure):
        with torch.enable_grad(), patch_backward():
            loss = closure()

        params, grads = [], []
        for group in self.param_groups:
            for p, g in self.split_p_and_g_in_group(group, skip_none=True, raw=True):
                params.append(p)
                grads.append(g)

        if not params:
            raise ValueError("No parameter has gradients")

        vs = [torch.randn_like(p) for p in params]
        with torch.enable_grad():
            try:
                hvs = torch.autograd.grad(grads, params, vs, create_graph=False, retain_graph=False, allow_unused=True)
            except RuntimeError as e:
                raise ExactHVPFailed(str(e.args))

        unused = []
        for p, g, v, hv in zip(params, grads, vs, hvs):
            p.hessian_vector = detach(hv)
            p.grad = detach(g)
            p.vector = detach(v)
            if hv is None:
                unused.append(list(p.shape))

        if unused:
            raise ExactHVPFailed(f"Parameters with the following shapes have no 2nd order derivative: {unused}")

        return loss

    def _handle_closure(self, closure):
        hessian_approx = self.hessian_approx and self._is_preconditioning

        if closure is None:
            if hessian_approx:
                raise ValueError("Hessian approximation requires a closure.")
            return None

        step = self._inner_group["total_hvp_steps"] = self._inner_group.get("total_hvp_steps", 0) + 1
        if not hessian_approx or step % self.hvp_interval == 0:
            with torch.enable_grad():
                loss = closure()
            return loss

        if self.finite_differences or self._fallback_enabled:
            return self._finite_differences_hvp(closure)

        try:
            return self._double_backward_hvp(closure)
        except NotImplementedError as e:
            if not self.fallback_to_finite_differences:
                raise
            if not any(isinstance(arg, str) and _cudnn_double_backward_pattern.match(arg) for arg in e.args):
                raise
            warn_once(
                "CUDNN doesn't support double-backward for some models (including RNNs). "  #
                f"Falling back to finite_differences.\n{_fd_error}{e}"
            )
        except RuntimeError as e:
            if not self.fallback_to_finite_differences:
                raise
            if not any(isinstance(arg, str) and _torch_compile_double_backward_pattern.match(arg) for arg in e.args):
                raise
            warn_once(
                f"torch.compile does not support double-backward. Disabling it may be beneficial, depending on "
                f"the model.\n{_fd_error}{e}"
            )
        except ExactHVPFailed as e:
            if not self.fallback_to_finite_differences:
                raise
            warn_once(f"Exact HVP calculation failed.\n{_fd_error}{e}")
        self._fallback_enabled = True
        return self._handle_closure(closure)

    def step(self, closure: Optional[Callable] = None):
        if self.precond_schedule is None:
            self._is_preconditioning = False
        else:
            self._is_preconditioning = psgd_should_update(self._inner_group, self.precond_schedule, self._precond_rng)
        loss = self._handle_closure(closure)

        # we assume that parameters are constant and that there are no excessive recompiles
        with torch.no_grad(), torch._dynamo.utils.disable_cache_limit():
            for group in self.param_groups:
                group["is_preconditioning"] = self._is_preconditioning
                self._step(group)
                if self.use_ema:
                    self.ema_update()
                for real, views in self.mapping.items():
                    for tensor in (real, *views):
                        for key in ("grad", "vector", "hessian_vector", "orig"):
                            if hasattr(tensor, key):
                                setattr(tensor, key, None)
        return loss


def copy_stochastic_list_(target: List[Tensor], source: List[Tensor]):
    for t, s in zip(target, source):
        copy_stochastic_(t, s)


@decorator_knowngood
def _lerp(state: List[Tensor], grad: List[Tensor], beta):
    ea32 = list(map(promote, state))
    grad = list(map(promote, grad))
    beta = promote(beta)
    stochastic_lerp_(ea32, grad, 1 - beta)
    copy_stochastic_list_(state, ea32)
    return ea32


@decorator_knowngood
def _compilable_adam_(
    exp_avg: List[Tensor],
    exp_avg_sq: List[Tensor],
    grad: List[Tensor],
    beta1: Tensor,
    beta2: Tensor,
    step: Tensor,
    eps: Tensor,
):
    beta1 = beta_debias(beta1, step)
    beta2 = beta_debias(beta2, step)

    g32 = list(map(promote, grad))
    exp_avg32 = _lerp(exp_avg, g32, beta1)
    denom = _compilable_exp_avg_sq_(exp_avg_sq, g32, beta2, eps, [None])
    u32 = torch._foreach_div(exp_avg32, denom)
    copy_stochastic_list_(grad, u32)


def adam_(
    exp_avg: List[Tensor],
    exp_avg_sq: List[Tensor],
    grad: List[Tensor],
    beta1: float,
    beta2: float,
    step: int,
    eps: float = 1e-8,
):
    exp_avg, exp_avg_sq, grad = map(list_guard, (exp_avg, exp_avg_sq, grad))
    beta1, beta2, step, eps = scalar_guard(beta1, beta2, step, eps, exp_avg[0])
    _compilable_adam_(exp_avg, exp_avg_sq, grad, beta1, beta2, step, eps)
    return grad


@decorator_knowngood
def _fused_compilable_adam_(
    y: List[Tensor],
    exp_avg: List[Tensor],
    exp_avg_sq: List[Tensor],
    update: List[Tensor],
    grad: List[Tensor],
    beta1: Tensor,
    beta2: Tensor,
    step: Tensor,
    decay: Tensor,
    lr: Tensor,
    eps: Tensor,
    caution: bool,
):
    beta1 = beta_debias(beta1, step)
    beta2 = beta_debias(beta2, step)

    u32, g32 = [list(map(promote, x)) for x in [update, grad]]
    exp_avg32 = _lerp(exp_avg, u32, beta1)
    denom = _compilable_exp_avg_sq_(exp_avg_sq, u32, beta2, eps, [None])
    u32 = torch._foreach_div(exp_avg32, denom)
    _compilable_update_(y, u32, decay, lr, caution, g32)


def fused_adam_(
    y: List[Tensor],
    exp_avg: List[Tensor],
    exp_avg_sq: List[Tensor],
    update: List[Tensor],
    grad: List[Tensor],
    beta1: float,
    beta2: float,
    step: int,
    lr: float,
    eps: float,
    decay: float,
    caution: bool,
):
    y, exp_avg, exp_avg_sq, grad = list_guard(y, exp_avg, exp_avg_sq, grad)
    beta1, beta2, step, lr = scalar_guard(beta1, beta2, step, lr, y[0])
    _fused_compilable_adam_(y, exp_avg, exp_avg_sq, update, grad, beta1, beta2, step, decay, lr, eps, caution)


@decorator_knowngood
def _compilable_laprop_(
    exp_avg: List[Tensor],
    exp_avg_sq: List[Tensor],
    grad: List[Tensor],
    beta1: Tensor,
    beta2: Tensor,
    step: Tensor,
    eps: Tensor,
):
    beta1 = beta_debias(beta1, step)
    beta2 = beta_debias(beta2, step)

    gp32 = list(map(promote, grad))
    denom = _compilable_exp_avg_sq_(exp_avg_sq, gp32, beta2, eps, [None])
    gp32 = torch._foreach_div(gp32, denom)
    gp32 = _lerp(exp_avg, gp32, beta1)
    copy_stochastic_list_(grad, gp32)


def laprop_(
    exp_avg: List[Tensor],
    exp_avg_sq: List[Tensor],
    grad: List[Tensor],
    beta1: float,
    beta2: float,
    step: int,
    eps: float = 1e-8,
):
    exp_avg, exp_avg_sq, grad = list_guard(exp_avg, exp_avg_sq, grad)
    beta1, beta2, step, eps = scalar_guard(beta1, beta2, step, eps, exp_avg[0])
    _compilable_laprop_(exp_avg, exp_avg_sq, grad, beta1, beta2, step, eps)
    return grad


@decorator_knowngood
def _fused_compilable_laprop_(
    y: List[Tensor],
    exp_avg: List[Tensor],
    exp_avg_sq: List[Tensor],
    update: List[Tensor],
    grad: List[Tensor],
    beta1: Tensor,
    beta2: Tensor,
    step: Tensor,
    lr: Tensor,
    decay: Tensor,
    caution: bool,
    eps: Tensor,
):
    beta1 = beta_debias(beta1, step)
    beta2 = beta_debias(beta2, step)

    u32, gp32 = [list(map(promote, x)) for x in [update, grad]]
    denom = _compilable_exp_avg_sq_(exp_avg_sq, u32, beta2, eps, [None])
    u32 = torch._foreach_div(u32, denom)
    u32 = _lerp(exp_avg, u32, beta1)
    _compilable_update_(y, u32, decay, lr, caution, gp32)


def fused_laprop_(
    y: List[Tensor],
    exp_avg: List[Tensor],
    exp_avg_sq: List[Tensor],
    update: List[Tensor],
    grad: List[Tensor],
    beta1: float,
    beta2: float,
    step: int,
    lr: float,
    decay: float,
    caution: bool,
    eps: float = 1e-8,
):
    exp_avg, exp_avg_sq, grad, y = list_guard(exp_avg, exp_avg_sq, grad, y)
    beta1, beta2, step, lr, eps = scalar_guard(beta1, beta2, step, lr, eps, exp_avg[0])
    _fused_compilable_laprop_(y, exp_avg, exp_avg_sq, update, grad, beta1, beta2, step, lr, decay, caution, eps)


@decorator_knowngood
def _fused_compilable_adopt_(y, update, grad, exp_avg_sq, exp_avg, beta1, beta2, step, lr, eps, decay, caution):
    u32, g32, exp_avg_sq32 = [list(map(promote, x)) for x in [update, grad, exp_avg_sq]]
    _compilable_update_(y, u32, decay, lr, caution, g32)

    beta1 = beta_debias(beta1, step)
    denom = [eps_sqrt(d, eps) for d in exp_avg_sq32]
    stochastic_lerp_(exp_avg, torch._foreach_div(g32, denom), 1 - beta1)

    beta2 = beta_debias(beta2, step + 1)
    stochastic_lerp_(exp_avg_sq, torch._foreach_mul(g32, g32), 1 - beta2)


def fused_adopt_(y, update, grad, exp_avg_sq, exp_avg, beta1, beta2, step, lr, eps, decay, caution):
    exp_avg, exp_avg_sq, grad, y = list_guard(exp_avg, exp_avg_sq, grad, y)
    beta1, beta2, step, lr = scalar_guard(beta1, beta2, step, lr, exp_avg[0])
    _fused_compilable_adopt_(y, update, grad, exp_avg_sq, exp_avg, beta1, beta2, step, lr, eps, decay, caution)


@decorator_knowngood
def _compilable_adopt_(grad, exp_avg_sq, exp_avg, beta1, beta2, step, eps):
    g32, exp_avg_sq32 = [list(map(promote, x)) for x in [grad, exp_avg_sq]]
    update = [e.clone() for e in exp_avg]

    beta1 = beta_debias(beta1, step)
    denom = [eps_sqrt(d, eps) for d in exp_avg_sq32]
    stochastic_lerp_(exp_avg, torch._foreach_div(g32, denom), 1 - beta1)

    stochastic_lerp_(exp_avg_sq, torch._foreach_mul(g32, g32), 1 - beta2)

    copy_stochastic_list_(grad, update)


def adopt(grad, exp_avg_sq, exp_avg, beta1, beta2, step, eps: float = 1e-8):
    exp_avg, exp_avg_sq, grad = list_guard(exp_avg, exp_avg_sq, grad)
    beta1, beta2, step, eps = scalar_guard(beta1, beta2, step, eps, exp_avg[0])
    _compilable_adopt_(grad, exp_avg_sq, exp_avg, beta1, beta2, step, eps)
    return grad


def stochastic_round_list_(ref: List[Tensor], source: List[Tensor]):
    return [stochastic_round_(r, s) for r, s in zip(ref, source)]


@decorator_knowngood
def stochastic_round_(ref: Tensor, source: Tensor):
    if source.dtype == torch.bfloat16 or ref.dtype == source.dtype:
        return source
    if ref.dtype != torch.bfloat16:
        return source.to(ref.dtype)
    result = torch.randint_like(source, dtype=torch.int32, low=0, high=(1 << 16))
    result.add_(source.view(dtype=torch.int32))
    result.bitwise_and_(-65536)  # -65536 = FFFF0000 as a signed int32
    return result.view(dtype=torch.float32).bfloat16()


@decorator_knowngood
def _compilable_copy_stochastic_(target: Tensor, source: Tensor):
    target.copy_(stochastic_round_(target, source))


def copy_stochastic_(target: Tensor, source: Tensor):
    if target.dtype == torch.bfloat16 and source.dtype in (torch.float16, torch.float32, torch.float64):
        _compilable_copy_stochastic_(target, source.float())
    set_(target, source)


@decorator_knowngood
def _compilable_update_(
    p: List[Tensor], u: List[Tensor], decay: Tensor, lr: Tensor, caution: bool, g: List[Optional[Tensor]]
):
    for u_, g_, p_ in zip(u, g, p):  # lr is data-dependent -> can't compile a foreach
        u_ = promote(u_.view_as(p_))
        p32_ = promote(p_)
        if caution:
            u_ = _compilable_cautioning(promote(g_), u_)
        p32_ = p32_ * (1 - decay * lr) + u_ * -lr
        copy_stochastic_(p_, p32_)


def update_param_(
    param: List[Tensor], update: List[Tensor], lr: float, decay: float, caution: bool = False, grad: List[Tensor] = None
):
    param, update, grad = list_guard(param, update, grad)
    lr = scalar_guard(lr, param[0])
    if not caution:
        grad = [None] * len(param)
    _compilable_update_(param, update, decay, lr, caution, grad)


def precond_schedule(step, precond_scheduler):
    precond_prob = max(step, 1) ** precond_scheduler[0]
    precond_prob = math.log10(precond_prob)
    precond_prob = precond_prob ** precond_scheduler[1] + 1
    return 1 / precond_prob


def get_soap_precond_schedule(precond_scheduler):
    return functools.partial(precond_schedule, precond_scheduler=precond_scheduler)


def _max_idx(x: List[int]):
    return len(x) - 1 - np.argmax(x[::-1])  # we want to start counting from the back, as torch is fan-out/fan-in


@decorator_knowngood
def stable_exp(x: Tensor):
    # fp16:
    #   exp(x) is stable in [-17, 11]
    #   `stable_exp` extends to [-17, 17]
    #   average error (in [-10, 10]) increased from 2.288e-3 to 2.299e-3
    # fp32:
    #   exp(x) is stable in [-103, 88]
    #   `stable_exp` extends to [-103, 103]
    #   average error (in [-87, 87]) reduced from 3.309-06 to 3.224-06
    return torch.where(x > 0, 1 / (-x).exp(), x.exp())


@decorator_knowngood
def mean_root(x: torch.Tensor, pow: float, eps=1e-12):
    # 1 / (mean(x ** pow) ** (1 / pow / 2))
    log_x = x.double().abs().clamp(min=eps).log()
    log_mean_x_pow = (log_x * pow).logsumexp(dim=0) - math.log(x.numel())
    return stable_exp(-log_mean_x_pow / pow / 2)


@decorator_knowngood
def divided_root(x: torch.Tensor, y: torch.Tensor, pow0: float, pow1: float, eps=1e-12):
    # mean(x ** pow0) ** (1 / pow0 / 2) / mean(y ** pow1) ** (1 / pow1 / 2)
    log_x = x.double().abs().clamp(min=eps).log()
    log_y = y.double().abs().clamp(min=eps).log()

    x_normed = (log_x * pow0).logsumexp(dim=0) - math.log(x.numel())
    x_normed = x_normed / pow0 / 2

    y_normed = (log_y * pow1).logsumexp(dim=0) - math.log(y.numel())
    y_normed = y_normed / pow1 / 2

    return stable_exp(x_normed - y_normed)


def precond_init_scale(scale, scale_scale, grad, hessian_vector, vector, scale_max: float = 1e6):
    automatic_scale = True
    manual_hint = " Set it manually using `precond_init_scale=0.1`"
    if scale is not None:
        automatic_scale = False
        warn_once(
            "It's recommended to use precond_init_scale=None (default since 1.7.x), which uses advanced heuristics."
        )
        if scale_scale is not None and scale_scale != 1:
            warn_once(
                "precond_init_scale_scale multiplies the precond_init_scale by a constant factor. With a fixed precond_init_scale, you should explicitly multiply it into the precond_init_scale."
            )
    elif hessian_vector is None:
        scale = mean_root(grad, 4) * scale_scale
    else:
        scale = divided_root(vector, hessian_vector, 2, 4) * scale_scale
    if isinstance(scale, torch.Tensor):
        scale = scale.item()  # slow, but necessary
    if np.isfinite(scale):
        if scale > scale_max or scale < 1 / scale_max:
            warn_once(f"The computed precond_init_scale {scale} is outside of the expected range.{manual_hint}")
        return scale
    if not automatic_scale:
        raise ValueError("The manually set precond_init_scale is not finite")

    for x in (grad, hessian_vector, vector):
        if x is None:
            continue
        if torch.allclose(x, torch.zeros_like(x)).item():
            raise ValueError(f"Grad or HVP is all 0s, causing NaNs in precond_init_scale computation.{manual_hint}")
        if not torch.isfinite(x).all().item():
            raise ValueError("Grad or HVP is not finite")
    raise ValueError(f"Computed precond_init_scale is not finite.{manual_hint}")


def init_lra(grad, scale, scale_scale, rank, hessian_vector, vector, dtype=None):
    scale = precond_init_scale(scale, scale_scale, grad, hessian_vector, vector)
    U = torch.randn((*grad.shape, rank), dtype=dtype, device=grad.device)
    V = torch.randn((*grad.shape, rank), dtype=dtype, device=grad.device)
    d = torch.full_like(grad, scale, dtype=dtype, device=grad.device)
    return U, V, d


def init_Q_exprs(
    grad, scale, scale_scale, max_size, min_ndim_triangular, memory_save_mode, hessian_vector, vector, dtype=None
):
    """
    For a scalar or tensor `grad`, we initialize its preconditioner Q and
    reusable einsum expressions for updating Q and preconditioning gradient.

    precond init scale computation from
    https://github.com/lixilinx/psgd_torch/blob/1943e66596111e78157ca1b72b31c1dfdf0653ef/preconditioned_stochastic_gradient_descent.py#L2208-L2227
    """
    scale = precond_init_scale(scale, scale_scale, grad, hessian_vector, vector)
    letters = string.ascii_lowercase + string.ascii_uppercase
    dtype = dtype if dtype is not None else grad.dtype
    shape = grad.shape

    if len(shape) == 0:  # scalar
        Q = [scale * torch.ones_like(grad, dtype=dtype)]
        exprA = ",->"
        exprGs = [",->"]
        exprP = ",,->"
        return [Q, (exprA, tuple(exprGs), exprP)]

    # Tensor
    if len(shape) > 13:
        raise ValueError(f"Got tensor with dim {len(grad.shape)}; Einstein runs out of letters!")

    scale = scale ** (1 / len(shape))

    dim_diag = [False for _ in shape]
    if memory_save_mode is None:
        pass
    elif memory_save_mode == "one_diag":
        dim_diag[_max_idx(shape)] = True
    elif memory_save_mode == "smart_one_diag":
        sorted_shape = sorted(shape)
        if len(shape) >= 2 and sorted_shape[-1] > sorted_shape[-2]:
            dim_diag[_max_idx(shape)] = True
    elif memory_save_mode == "all_diag":
        dim_diag = [True for _ in shape]
    else:
        raise ValueError(
            f"Invalid memory_save_mode: {memory_save_mode}, must be one of "
            "[None, 'one_diag', 'all_diag', 'smart_one_diag']"
        )

    Q = []
    piece1A, piece2A, piece3A = ([], "", "")
    exprGs = []
    piece1P, piece2P, piece3P, piece4P = ([], [], "", "")
    for i, (size, dim_d) in enumerate(zip(shape, dim_diag)):
        if size == 1 or size > max_size or len(shape) < min_ndim_triangular or dim_d:
            # use diagonal matrix as preconditioner for this dim
            Q.append(scale * torch.ones(size, dtype=promote(dtype), device=grad.device))

            piece1A.append(letters[i])
            piece2A = piece2A + letters[i]
            piece3A = piece3A + letters[i]
            piece1 = "".join([(letters[i + 13] if j == i else letters[j]) for j in range(len(shape))])
            subscripts = piece1 + "," + piece1 + "->" + letters[i + 13]
            exprGs.append(subscripts)
            piece1P.append(letters[i + 13])
            piece2P.append(letters[i + 13])
            piece3P = piece3P + letters[i + 13]
            piece4P = piece4P + letters[i + 13]
        else:
            # use triangular matrix as preconditioner for this dim
            Q.append(scale * torch.eye(size, dtype=dtype, device=grad.device))
            piece1A.append(letters[i] + letters[i + 13])
            piece2A = piece2A + letters[i + 13]
            piece3A = piece3A + letters[i]
            piece1 = "".join([(letters[i + 13] if j == i else letters[j]) for j in range(len(shape))])
            piece2 = "".join([(letters[i + 26] if j == i else letters[j]) for j in range(len(shape))])
            subscripts = piece1 + "," + piece2 + "->" + letters[i + 13] + letters[i + 26]
            exprGs.append(subscripts)
            a, b, c = (letters[i], letters[i + 13], letters[i + 26])
            piece1P.append(a + b)
            piece2P.append(a + c)
            piece3P = piece3P + c
            piece4P = piece4P + b

    exprA = ",".join(piece1A) + "," + piece2A + "->" + piece3A
    exprP = ",".join(piece1P) + "," + ",".join(piece2P) + "," + piece3P + "->" + piece4P
    return [Q, (exprA, tuple(exprGs), exprP)]


@decorator
def psgd_balance_Q(Q_in):
    norms = torch.stack([q.norm(float("inf")) for q in Q_in])
    geometric_mean = norms.log().mean().exp()
    norms = geometric_mean / norms
    torch._foreach_mul_(Q_in, list(norms))


@decorator
def psgd_balance_lra(U: Tensor, V: Tensor):
    u_norm = promote(torch.linalg.vector_norm(U))
    v_norm = promote(torch.linalg.vector_norm(V))
    scale = (u_norm / v_norm) ** 0.5
    U.div_(scale)
    V.mul_(scale)


@decorator
def low_rank_mm(U: Tensor, V: Tensor, x: Tensor) -> Tensor:
    dtype = min_dtype([U, V, x])
    return x + torch.einsum("br,gr,g->b", U.to(dtype), V.to(dtype), x.to(dtype)).to(x.dtype)


def update_lra_precond_(
    U: List[Tensor],
    V: List[Tensor],
    d: List[Tensor],
    vector: Tensor,
    hessian_vector: Tensor,
    eps: float,
    step: float,
    delayed: bool,
):
    """
    Adapted from https://github.com/lixilinx/psgd_torch/blob/6dbea94915679d08a289928e6431b6ce07931aaf/preconditioned_stochastic_gradient_descent.py#L657
    """
    U_orig, V_orig, d_orig = U, V, d

    U, V, d = flatten(U, 1), flatten(V, 1), flatten(d)

    dtype = min_dtype([U, V, vector, hessian_vector])
    U, V, vector, hessian_vector = U.to(dtype), V.to(dtype), vector.to(dtype), hessian_vector.to(dtype)

    eps = scalar_guard(eps, vector)

    Qh = low_rank_mm(U, V, d * hessian_vector)
    Ph = d * low_rank_mm(V, U, Qh)
    rank = U.size(1)

    VtU = torch.einsum("br,bn->rn", V, U)  # (rank, rank)
    I = torch.eye(rank, dtype=VtU.dtype, device=VtU.device)
    IpVtU = I + VtU
    invQtv = vector / d

    # LU factorization to reuse computation
    try:
        LU, pivots = torch.linalg.lu_factor(IpVtU)
    except RuntimeError:
        # Error:
        # U[2,2] is zero and using it on lu_solve would result in a division by zero.
        # If you still want to perform the factorization, consider calling
        # linalg.lu(A, pivot) or linalg.lu_factor_ex(A, pivot)
        # ---
        # So, we skip this step and reattempt on the next one
        return U.to(U_orig[0].dtype), V.to(V_orig[0].dtype), d.to(d_orig[0].dtype)

    invQtv = invQtv - V @ torch.linalg.lu_solve(LU, pivots, (U.T @ invQtv).view(-1, 1), adjoint=True).flatten()
    invPv = invQtv - U @ torch.linalg.lu_solve(LU, pivots, (V.T @ invQtv).view(-1, 1)).flatten()
    invPv = invPv / d

    nablaD = Ph * hessian_vector - vector * invPv
    divisor = (Ph.square() + vector.square()) * (hessian_vector.square() + invPv.square())
    divisor = divisor.add(eps).sqrt().max()
    d_step = step / divisor

    apply_flat_add(d_orig, d * nablaD, -d_step)

    a, b = Qh, invQtv

    precond_u = random.random() < 0.5  # update either U or V, not both at the same time
    precond = V if precond_u else U
    atV = torch.einsum("b,br->r", a, precond)  # o == one
    btV = torch.einsum("b,br->r", b, precond)
    atVVt = torch.einsum("r,br->b", atV, precond)
    btVVt = torch.einsum("r,br->b", btV, precond)
    precond_step = step / (a.norm() * atVVt.norm() + b.norm() * btVVt.norm() + eps)
    if precond_u:
        a = torch.einsum("b,r,rg->bg", a, atV, IpVtU)
        b = torch.einsum("b,r,rg->bg", b, btV, IpVtU)
    else:
        a = a + torch.einsum("br,r->b", V, atV)
        b = b + torch.einsum("br,r->b", V, btV)
        a = torch.einsum("b,r->br", a, atV)
        b = torch.einsum("b,r->br", b, btV)
    apply_flat_add(U_orig if precond_u else V_orig, b - a, precond_step)

    if not delayed:
        stochastic_add_([d], [d * nablaD], -d_step)
        stochastic_add_([U if precond_u else V], [b - a], precond_step)
    return U.to(U_orig[0].dtype), V.to(V_orig[0].dtype), d.to(d_orig[0].dtype)


def lra_precond(U, V, d, g):
    """
    As-is from https://github.com/lixilinx/psgd_torch/blob/6dbea94915679d08a289928e6431b6ce07931aaf/preconditioned_stochastic_gradient_descent.py#L744
    """
    g = low_rank_mm(U, V, d * g)
    return d * low_rank_mm(V, U, g)


@decorator_knowngood
def dampen_grad(g: Tensor, damp: float = 2**-13):
    # https://github.com/lixilinx/psgd_torch/blob/1943e66596111e78157ca1b72b31c1dfdf0653ef/preconditioned_stochastic_gradient_descent.py#L50
    v = torch.randn_like(g)
    return v, g + damp * g.abs().mean() * v


@decorator_knowngood
def apply_lra_update(params: List[Tensor], update: Tensor, U: Tensor, V: Tensor, d: Tensor):
    update = lra_precond(U, V, d, update)
    start = 0
    update = update.flatten()
    for p in params:
        size = p.numel()
        copy_stochastic_(p, update[start : start + size].view_as(p))
        start += size


@decorator_knowngood
def apply_flat_update(params: List[Tensor], update: Tensor):
    start = 0
    update = update.flatten()
    for p in params:
        size = p.numel()
        copy_stochastic_(p, update[start : start + size].view_as(p))
        start += size


@decorator_knowngood
def apply_flat_add(params: List[Tensor], update: Tensor, alpha: Tensor):
    start = 0
    update = update.flatten()
    for p in params:
        size = p.numel()
        stochastic_add_([p], [update[start : start + size].view_as(p)], alpha)
        start += size


@decorator_knowngood
def extract_from_flat_update(params: List[Tensor], update: Tensor):
    start = 0
    outputs = []
    update = update.flatten()
    for p in params:
        size = p.numel()
        outputs.append(update[start : start + size].view_as(p))
        start += size
    return outputs


@decorator_knowngood
def flatten(x: List[Tensor], remaining: int = 0) -> Tensor:
    last_dim = x[0].shape[-remaining:] if remaining else []
    return torch.cat([i.reshape(-1, *last_dim) for i in x], 0)


@decorator_knowngood
def dampen_multiple(g: List[Tensor], damp: float = 2**-13):
    vs = []
    gs = []
    for g_ in g:
        v, g = dampen_grad(g_, damp)
        vs.append(v)
        gs.append(g)
    return flatten(vs), flatten(gs)


@decorator_knowngood
def casted_einsum(expr: str, *args: Tensor) -> Tensor:
    md = min_dtype(args)
    return torch.einsum(expr, *[a.to(md) for a in args]).to(args[-1].dtype)


def psgd_calc_A_and_conjB(exprA, G, Q, conjB):  # conjB ("V", "vector") == randn during hvp/whitening
    order = G.dim()
    if order > 1:
        conjB = conjB.view_as(G).permute(*range(1, order), 0)
    conjB = conjB.to(promote(G.dtype))
    A = casted_einsum(exprA, *Q, G)
    for i, q in enumerate(Q):
        q = promote(q)
        if q.dim() <= 1:
            conjB /= q
        else:
            solved = torch.linalg.solve_triangular(q, conjB.reshape(-1, q.size(0)).contiguous(), upper=True, left=False)
            conjB = solved.reshape_as(conjB)
        if i < order - 1:
            conjB = conjB.transpose(i, -1)
    return A, conjB


def psgd_lb(A, max_abs):
    A /= max_abs
    a0 = torch.einsum("ij,ij->j", A, A)
    i = torch.argmax(a0)
    x = torch.index_select(A, 1, i).flatten().contiguous()
    x = torch.einsum("i,ij->j", x, A)
    x /= x.norm()
    x = torch.einsum("j,kj->k", x, A)
    x = x.norm()
    x *= max_abs
    return x


@decorator
def psgd_update_precond(Q, exprs, G, precond_lr, oq, store_triu_as_line, V):
    """Update Kronecker product preconditioner Q with pair (V, G)."""
    exprA, exprGs, _ = exprs
    A, conjB = psgd_calc_A_and_conjB(exprA, G, Q, V)

    for q, exprG, o in zip(Q, exprGs, oq):
        term1 = promote(torch.einsum(exprG, A, A))
        term2 = promote(torch.einsum(exprG, conjB, conjB))
        term1, term2 = term1 - term2, term1 + term2
        term1 *= precond_lr
        norm = term2.norm(float("inf"))
        if q.dim() < 2:
            term1 *= q.to(term1.dtype) / norm.clamp_(min=tiny_bf16)
        else:
            torch.triu(term1, out=term1)
            term1 /= torch.where(norm > 0, psgd_lb(term2, norm), norm).clamp_(tiny_bf16)
            term1 = torch.mm(term1, q.to(term1.dtype))
        if store_triu_as_line:
            term1 = triu_to_line([term1])[0][1]  # Convert update to line format
            # Apply update directly to the tensor part of the state tuple o[1]
            stochastic_add_(o[1], term1, -1)
        else:
            # Apply update to the state tensor o
            stochastic_add_(o, term1, -1)


@decorator_knowngood
def _compilable_l2_clip_(x, clip_at):
    ref = x
    x = list(map(promote, x))
    norm = torch._foreach_norm(x)
    torch._foreach_maximum_(norm, clip_at)
    out = torch._foreach_div(x, norm)
    return stochastic_round_list_(ref, out)


def l2_normalization_(x, clip_at: float = 1e-8):
    x = list_guard(x)
    return _compilable_l2_clip_(x, clip_at)


def l2_clip_(x, clip_at: float = 1.0):
    x = list_guard(x)
    return _compilable_l2_clip_(x, clip_at)


@decorator_knowngood
def _compilable_rmsnorm_clip_(x, clip_at):
    x = list(map(promote, x))
    norm = torch._foreach_norm(x)
    norm = [n.div_(x_.numel() ** 0.5) for n, x_ in zip(norm, x)]
    torch._foreach_maximum_(norm, clip_at)
    return torch._foreach_div(x, norm)


def rmsnorm_clip_(x, clip_at: float = 1.0):
    x = list_guard(x)
    return _compilable_rmsnorm_clip_(x, clip_at)


def rmsnorm_normalize_(x, clip_at: float = 1e-6):
    x = list_guard(x)
    return _compilable_rmsnorm_clip_(x, clip_at)


@decorator_knowngood
def _compilable_mu_law_compress_(x, mu):
    """
    original at https://github.com/opooladz/modded-nanogpt-psgd/blob/dc7c78082ac15fbf326f1bacd9e0ead0a2b45908/kron_mu.py
    """

    for x_ in x:
        xa = promote(x_.abs()) * mu
        xa = xa.log1p()
        xa = xa / math.log1p(mu)
        xa = xa.copysign(x_)
        copy_stochastic_(x_, xa)


def mu_law_compress(x, mu=127.0):
    """
    μ-law compression
    Args:
        x: Input tensor
        mu: Compression parameter (default 127.0 for behavior similar to trust_region=1.5)
    """
    x = list_guard(x)
    mu = scalar_guard(mu, x[0])
    _compilable_mu_law_compress_(x, mu)
    return x


@decorator_knowngood
def _compilable_a_law_compress_(x, A):
    """
    original at https://github.com/opooladz/modded-nanogpt-psgd/blob/dc7c78082ac15fbf326f1bacd9e0ead0a2b45908/kron_mu.py
    """
    for x_ in x:
        xa = promote(x_.abs()) * A
        xa = torch.where(xa < 1, xa, 1 + xa.log())
        xa = xa.copysign(x_)
        xa = xa * (1 / (1 + math.log(A)))
        copy_stochastic_(x_, xa)


def a_law_compress(x, A=87.6):
    """
    A-law compression
    Args:
        x: Input tensor
        A: Compression parameter (default 87.6 - European PCM standard)
    :param x:
    :param A:
    :return:
    """
    x = list_guard(x)
    A = scalar_guard(A, x[0])
    _compilable_a_law_compress_(x, A)
    return x


def identity(x):
    return x


@decorator_knowngood
def _compilable_weight_decay_to_ema_(p, ema, ema_decay, weight_decay):
    ema32 = _lerp(ema, p, ema_decay)
    _lerp(p, ema32, 1 - weight_decay)


def weight_decay_to_ema_(p, ema, ema_decay, weight_decay):
    p, ema = list_guard(p, ema)
    ema_decay, weight_decay = scalar_guard(ema_decay, weight_decay, p[0])
    _compilable_weight_decay_to_ema_(p, ema, ema_decay, weight_decay)


@decorator_knowngood
def _compilable_l1_weight_decay_to_ema_(p, ema, ema_decay, weight_decay):
    ema32 = _lerp(ema, p, ema_decay)
    for p_, e_ in zip(p, ema32):
        p32 = promote(p_)
        p32 = p32 + (p32 - e_).sign() * weight_decay
        copy_stochastic_(p_, p32)


def l1_weight_decay_to_ema_(p, ema, ema_decay, weight_decay):
    p, ema = list_guard(p, ema)
    ema_decay, weight_decay = scalar_guard(ema_decay, weight_decay, p[0])
    _compilable_l1_weight_decay_to_ema_(p, ema, ema_decay, weight_decay)


@decorator_knowngood
def _compilable_sign_(grad: List[Tensor], graft: bool):
    for g_ in grad:
        gs = g_.sign()
        if graft:
            gs = _compilable_grafting(g_, gs)
        copy_stochastic_(g_, gs)


def sign_(grad: List[Tensor], graft: bool = True):
    grad = list_guard(grad)
    _compilable_sign_(grad, graft)
    return grad


@decorator_knowngood
def _compilable_trust_region_clip_(grad, lerp, scale):
    # (sgn(x) * log(1 + |x|) * 0.1 + tanh(x) * 0.9).clamp_(min=-2, max=2)
    for x_ in grad:
        x = promote(x_)
        x = x / scale
        tanh = x.tanh()
        x = x.abs().log1p()
        x = x.copysign(tanh) * (1 - lerp) + tanh * lerp
        x = x * scale
        x = x.clamp(min=-2, max=2)
        copy_stochastic_(x_, x)


def trust_region_clip_(grad, lerp=0.9, scale=1.5):
    grad = list_guard(grad)
    lerp, scale = scalar_guard(lerp, scale, grad[0])
    _compilable_trust_region_clip_(grad, lerp, scale)
    return grad


@decorator
def triu_to_line(Q_list: List[Tensor]):
    out = []
    for q in Q_list:
        if q.dim() < 2:
            out.append((None, q))
        else:
            out.append((q.shape, q[tuple(torch.triu_indices(*q.shape))]))
    return out


def _triu_shape(numel):
    n = int((2 * numel) ** 0.5)
    assert n * (n + 1) == 2 * numel
    return n, n


@decorator
def line_to_triu(Q_list: List[Tuple[Optional[List[int]], Tensor]]):
    new = []
    for shape, q in Q_list:
        if shape is not None:
            shape = _triu_shape(q.numel())
            x = torch.zeros(shape, device=q.device, dtype=q.dtype)
            x[tuple(torch.triu_indices(*shape, device=q.device))] = q
            q = x
        new.append(q)
    return new


def update_triu_(q_state, materialised):
    for (shape0, q), (shape1, m) in zip(q_state, triu_to_line(materialised)):
        assert shape0 == shape1
        copy_stochastic_(q, m)


_warned = set()


def warn_once(msg):
    if msg not in _warned:
        warnings.warn(msg)
        _warned.add(msg)


def psgd_should_update(
    group, prob: Union[float, callable], rng: Optional[random.Random] = None, name: str = "cumulative_prob"
):
    group[f"{name}_prob_step"] = group.get(f"{name}_prob_step", 0) + 1
    if not isinstance(prob, float):
        prob = prob(group[f"{name}_prob_step"])
    if group["stochastic_schedule"]:
        return rng.random() < prob
    cumulative_prob = group.get(name, 0)
    group[name] = cumulative_prob + prob
    return int(group[name]) > int(cumulative_prob)


@decorator_knowngood
def precond_grad_cached_(
    expr: str, ea: Tensor, *cached_q: Tensor, caution: bool = False, grad: Optional[Tensor] = None, cast: bool = True
):
    if caution:
        ea = _compilable_cautioning(grad, ea)
    md = min_dtype(list(cached_q) + [ea])
    args = [q.to(md) for q in cached_q]
    args = args + [ea.to(md)]
    new = torch.einsum(expr, *args)
    if cast:
        return new.to(ea.dtype)
    return new


@decorator_knowngood
def _compilable_fused_precond_grad_cached_(expr: str, ea: Tensor, param, lr, grad, decay, caution, *cached_q: Tensor):
    precond = precond_grad_cached_(expr, ea, *cached_q, caution=caution, grad=grad, cast=False)
    update_param_(param, precond, lr, decay, caution=False)


def fused_precond_grad_cached_(expr: str, ea: Tensor, param, lr, grad, decay, caution, *cached_q: Tensor):
    lr = scalar_guard(lr, param[0])
    _compilable_fused_precond_grad_cached_(expr, ea, param, lr, grad, decay, caution, *cached_q)


@decorator_knowngood
def psgd_precond_grad(expr: str, ea: Tensor, *preconds: Tensor, caution: bool = False, grad: Optional[Tensor] = None):
    if caution:
        ea = _compilable_cautioning(grad, ea)
    md = min_dtype(list(preconds) + [ea])
    args = [q.to(md) for q in preconds]
    args = args + args + [ea.to(md)]
    new = torch.einsum(expr, *args)
    return new.to(ea.dtype)


@decorator_knowngood
def _compilable_fused_psgd_precond_grad(expr: str, ea: Tensor, param, lr, grad, decay, caution, *preconds: Tensor):
    precond = psgd_precond_grad(expr, ea, *preconds, caution=caution, grad=grad)
    update_param_(param, precond, lr, decay, caution=False, grad=grad)


def fused_psgd_precond_grad(expr: str, ea: Tensor, param, lr, grad, decay, caution, *preconds: Tensor):
    lr = scalar_guard(lr, param[0])
    _compilable_fused_psgd_precond_grad(expr, ea, param, lr, grad, decay, caution, *preconds)


@decorator_knowngood
def _compilable_mars_correction_(g: Tensor, old_g: Tensor, a: Tensor):
    g_copy = [g_.clone() for g_ in g]
    _compilable_stochastic_lerp_(g, old_g, a)
    copy_stochastic_list_(old_g, g_copy)


def mars_correction(g, old_g, beta1, gamma):
    a = -gamma * beta1 / (1 - beta1)
    g, old_g = list_guard(g), list_guard(old_g)
    a = scalar_guard(a, g[0])
    _compilable_mars_correction_(g, old_g, a)


@decorator_knowngood
def _compilable_orthogonalization(weight: List[Tensor], grad: List[Tensor], eps: Tensor, graft: bool = True):
    """
    Implements OrthoGrad from "Grokking at the Edge of Numerical Stability" (https://arxiv.org/abs/2501.04697)
    """

    for w, g in zip(weight, grad):
        proj = promote((w * g).sum()) / promote((w * w).sum()).add(eps)
        out = promote(g) - proj * promote(w)  # promote in this funky way to keep traffic minimal

        if graft:
            out = _compilable_grafting(g, out)
        copy_stochastic_(g, out)


def orthogonalize_grad_to_param(weight, grad, eps, graft=True):
    weight, grad = list_guard(weight, grad)
    eps = scalar_guard(eps, weight[0])
    _compilable_orthogonalization(weight, grad, eps, graft)
    return grad


@decorator_knowngood
def _compilable_cautioning(g: Tensor, update: Tensor):
    mask = g.signbit() ^ update.signbit()  # "Mask if they point in different directions"
    update = update.masked_fill(mask, 0)
    scale = mask.numel() / (mask.numel() - mask.sum()).clamp(min=1)
    update.mul_(scale)
    return update


def caution(g, update):
    return _compilable_cautioning(g, update)


def precond_update_prob_schedule(max_prob=1.0, min_prob=0.03, decay=0.999, flat_start=1000):
    """Anneal preconditioner update probability during beginning of training.

    PSGD benefits from more preconditioner updates at the beginning of training,
    but once the preconditioner is learned the update probability can drop low.

    This schedule is an exponential anneal with a flat start. Default settings keep
    update probability at `max_prob` for 1000 steps then exponentially anneal down to
    `min_prob` by ~4000 steps. Default settings work very well for most models and
    training regimes.
    """

    def _schedule(n):
        return max(min_prob, max_prob * decay ** max(n - flat_start, 0))

    return _schedule


def merge_group(group, *tensors):
    if not group.get("merge_dims", False):
        return tensors
    if isinstance(tensors[0], list):
        return [merge_group(group, *t) for t in tensors]

    out = []
    for t in tensors:
        append_or_extend(
            out,
            dim_merger(
                t,
                group["max_size_triangular"] if "max_size_triangular" in group else group["max_precond_dim"],
                group.get("split", False),
            ),
        )
    return out


@decorator_knowngood
def _compilable_d_adapt_(grads: List[Tensor], update: List[Tensor], state: List[Tensor], delta: List[Tensor]):
    for g_, u_, s_, d_ in zip(grads, update, state, delta):
        g, u, s, d = promote(g_), promote(u_), promote(s_), promote(d_)
        next_d = d * (g * s).sum()
        s = s + u * d
        next_d = next_d / s.abs().sum()
        next_d = torch.maximum(next_d, d)
        copy_stochastic_(u_, u * d)
        copy_stochastic_(d_, next_d)
        copy_stochastic_(s_, s)


def d_adaptation(grads: List[Tensor], update: List[Tensor], state: List[Tensor], delta: List[Tensor]):
    grads, update, state, delta = list_guard(grads, update, state, delta)
    _compilable_d_adapt_(grads, update, state, delta)


@decorator_knowngood
def _compilable_lr_adapt_(
    grads: List[Tensor], update: List[Tensor], state: List[Tensor], delta: List[Tensor], lr_lr: Tensor
):
    for g_, u_, s_, d_ in zip(grads, update, state, delta):
        g, u, s, d = promote(g_), promote(u_), promote(s_), promote(d_)
        lr_grad = d.sigmoid()
        lr_grad = lr_grad * (1 - lr_grad)
        lr_grad = lr_grad * (s * g).mean()
        d = d - lr_grad * lr_lr
        copy_stochastic_(d_, d)
        copy_stochastic_(u_, u * d.sigmoid())
        copy_stochastic_(s_, u)


def lr_adaptation(grads: List[Tensor], update: List[Tensor], state: List[Tensor], delta: List[Tensor], lr_lr: float):
    grads, update, state, delta = list_guard(grads, update, state, delta)
    lr_lr = scalar_guard(lr_lr, grads[0])
    _compilable_lr_adapt_(grads, update, state, delta, lr_lr)


@decorator_knowngood
def _compilable_pointwise_lr_adapt_(
    grads: List[Tensor], update: List[Tensor], state: List[Tensor], delta: List[Tensor], lr_lr: Tensor
):
    for g_, u_, s_, d_ in zip(grads, update, state, delta):
        g, u, s, d = promote(g_), promote(u_), promote(s_), promote(d_)
        lr_grad = d.sigmoid()
        lr_grad = lr_grad * (1 - lr_grad)
        lr_grad = lr_grad * s * g
        d = d - lr_grad * lr_lr
        copy_stochastic_(d_, d)
        copy_stochastic_(u_, u * d.sigmoid())
        copy_stochastic_(s_, u)


def pointwise_lr_adaptation(
    grads: List[Tensor], update: List[Tensor], state: List[Tensor], delta: List[Tensor], lr_lr: float
):
    grads, update, state, delta = list_guard(grads, update, state, delta)
    lr_lr = scalar_guard(lr_lr, grads[0])
    _compilable_lr_adapt_(grads, update, state, delta, lr_lr)


def hook_optimizer_into_model(model, optimizer, *args, **kwargs):
    optimizers = {}

    def _step(p: Tensor):
        o = optimizers[p]
        o.step()
        o.zero_grad()

    for p in model.parameters():
        optimizers[p] = optimizer([p], *args, **kwargs)
        p.register_post_accumulate_grad_hook(_step)

    return optimizers


def fused_hook(parameters, optimizer, *args, **kwargs):
    parameters = list(parameters)
    param_count = len(parameters)
    seen_params = set()

    o = optimizer(parameters, *args, **kwargs)
    step_fn = o.step
    o.step = functools.partial(
        warn_once, msg="You're trying to call `step` on a fused optimizer. This will not do anything."
    )

    def _step(p: Tensor):
        seen_params.add(p)

        if len(seen_params) < param_count:
            step_fn()
            o.zero_grad()
            seen_params.clear()

    for p in parameters:
        p.register_post_accumulate_grad_hook(_step)

    return o


@decorator_knowngood
def _compilable_caution_no_scale(g: Tensor, update: Tensor):
    mask = g.signbit() ^ update.signbit()  # "Mask if they point in different directions"
    update = update.masked_fill(mask, 0)
    return update


def disable_caution_scaling():
    global _compilable_cautioning
    _compilable_cautioning = _compilable_caution_no_scale
