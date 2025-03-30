import random
from typing import List, Optional

import torch
from torch import Tensor

from .. import utils
from ..utils import decorator, decorator_knowngood, min_dtype, scalar_guard, tiny_bf16

#############################
# PSGD LRA OPTIMIZATIONS
#############################


@decorator
def low_rank_mm_optimized(U: Tensor, V: Tensor, x: Tensor) -> Tensor:
    """Optimized version of low_rank_mm using fused operations and memory reuse"""
    dtype = min_dtype([U, V, x])
    # Convert only once and cache the result
    U_dt, V_dt, x_dt = U.to(dtype), V.to(dtype), x.to(dtype)

    # Use a more efficient implementation that avoids multiple conversions
    # torch.bmm can be more efficient than einsum for this specific pattern
    if U.dim() == 2:  # This is the common case (batch, rank)
        # Shape of result: (batch, )
        tmp = torch.mul(U_dt, x_dt.unsqueeze(-1)).sum(dim=0)  # (rank, )
        result = torch.mv(V_dt, tmp)  # (batch, )
        return result.to(x.dtype) + x
    else:
        # Fallback to original implementation for other dimensionalities
        return x + torch.einsum("br,gr,g->b", U_dt, V_dt, x_dt).to(x.dtype)


@torch.compile(mode="reduce-overhead")
def update_lra_precond_core(
    U: Tensor, V: Tensor, d: Tensor, vector: Tensor, hessian_vector: Tensor, eps: float, step: float, delayed: bool
):
    """Core computational part of update_lra_precond optimized with torch.compile"""
    # Here we apply torch.compile to the computational bottleneck
    # All inputs are already properly typed and processed

    Qh = low_rank_mm_optimized(U, V, d * hessian_vector)
    Ph = d * low_rank_mm_optimized(V, U, Qh)
    rank = U.size(1)

    # Cache VtU computation which is used multiple times
    VtU = torch.einsum("br,bn->rn", V, U)  # (rank, rank)
    I = torch.eye(rank, dtype=VtU.dtype, device=VtU.device)
    IpVtU = I + VtU
    invQtv = vector / d

    # LU factorization to reuse computation
    LU, pivots = torch.linalg.lu_factor(IpVtU)

    # Compute vectors inline to reduce memory allocation
    invQtv = invQtv - V @ torch.linalg.lu_solve(LU, pivots, (U.T @ invQtv).view(-1, 1), adjoint=True).flatten()
    invPv = invQtv - U @ torch.linalg.lu_solve(LU, pivots, (V.T @ invQtv).view(-1, 1)).flatten()
    invPv = invPv / d

    # Compute nabla D
    nablaD = Ph * hessian_vector - vector * invPv

    # Compute divisor more efficiently using fused operations
    Ph_squared = Ph.square()
    vector_squared = vector.square()
    hv_squared = hessian_vector.square()
    invPv_squared = invPv.square()

    divisor = (Ph_squared + vector_squared) * (hv_squared + invPv_squared)
    divisor = divisor.add(eps).sqrt().max()
    d_step = step / divisor

    # Compute for gradient update
    a, b = Qh, invQtv

    # Update either U or V, not both at the same time
    precond_u = random.random() < 0.5
    precond = V if precond_u else U

    # Cache computations that get reused
    atV = torch.einsum("b,br->r", a, precond)
    btV = torch.einsum("b,br->r", b, precond)
    atVVt = torch.einsum("r,br->b", atV, precond)
    btVVt = torch.einsum("r,br->b", btV, precond)

    # Compute step size
    precond_step = step / (a.norm() * atVVt.norm() + b.norm() * btVVt.norm() + eps)

    # Update precond matrix
    if precond_u:
        a_new = torch.einsum("b,r,rg->bg", a, atV, IpVtU)
        b_new = torch.einsum("b,r,rg->bg", b, btV, IpVtU)
    else:
        # Optimize with in-place operations where possible
        a_new = a + torch.einsum("br,r->b", V, atV)
        b_new = b + torch.einsum("br,r->b", V, btV)
        a_new = torch.einsum("b,r->br", a_new, atV)
        b_new = torch.einsum("b,r->br", b_new, btV)

    # Return updated values
    return d, nablaD, d_step, U if precond_u else V, b_new - a_new, precond_step, precond_u


def update_lra_precond_optimized(
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
    Optimized version of update_lra_precond_ with:
    1. Reduced memory allocations
    2. Fused operations
    3. Torch.compile for core computations
    4. Better caching of intermediate results
    """
    U_orig, V_orig, d_orig = U, V, d

    # Flatten once
    U_flat, V_flat, d_flat = utils.flatten(U, 1), utils.flatten(V, 1), utils.flatten(d)

    # Convert dtype once
    dtype = min_dtype([U_flat, V_flat, vector, hessian_vector])
    U_dt = U_flat.to(dtype)
    V_dt = V_flat.to(dtype)
    vector_dt = vector.to(dtype)
    hv_dt = hessian_vector.to(dtype)

    # Convert scalar once
    eps_tensor = scalar_guard(eps, vector)

    try:
        # Run optimized core computation with torch.compile
        d_flat, nablaD, d_step, precond, update, precond_step, precond_u = update_lra_precond_core(
            U_dt, V_dt, d_flat, vector_dt, hv_dt, eps, step, delayed
        )

        # Apply updates efficiently
        utils.apply_flat_add(d_orig, d_flat * nablaD, -d_step)
        utils.apply_flat_add(U_orig if precond_u else V_orig, update, precond_step)

        # For immediate updates
        if not delayed:
            utils.stochastic_add_([d], [d_flat * nablaD], -d_step)
            utils.stochastic_add_([U if precond_u else V], [update], precond_step)

        return U_flat.to(U_orig[0].dtype), V_flat.to(V_orig[0].dtype), d_flat.to(d_orig[0].dtype)

    except RuntimeError:
        # Fallback to original implementation on failure
        return utils.update_lra_precond_(U, V, d, vector, hessian_vector, eps, step, delayed)


@decorator
def lra_precond_optimized(U, V, d, g):
    """
    Optimized version of lra_precond using memory caching and fused operations
    """
    # Get the common dtype only once
    dtype = min_dtype([U, V, d, g])

    # Convert to this dtype once
    U_dt, V_dt, d_dt, g_dt = U.to(dtype), V.to(dtype), d.to(dtype), g.to(dtype)

    # First part: g_mid = d * g
    g_mid = d_dt * g_dt

    # Second part: Qh = low_rank_mm(U, V, g_mid)
    # Use optimized low_rank_mm
    Qh = low_rank_mm_optimized(U_dt, V_dt, g_mid)

    # Third part: result = d * low_rank_mm(V, U, Qh)
    result = d_dt * low_rank_mm_optimized(V_dt, U_dt, Qh)

    # Return result in original dtype
    return result.to(g.dtype)


#############################
# PSGD KRON OPTIMIZATIONS
#############################


@decorator
def psgd_calc_A_and_conjB_optimized(exprA, G, Q, conjB):
    """Optimized version of psgd_calc_A_and_conjB using torch.compile and memory reuse"""
    order = G.dim()
    if order > 1:
        conjB = conjB.view_as(G).permute(*range(1, order), 0)

    # Convert dtype once
    G_dtype = utils.promote(G.dtype)
    conjB = conjB.to(G_dtype)

    # Compute A using einsum (could be cached if called multiple times with same Q, G)
    A = utils.casted_einsum(exprA, *Q, G)

    # Process each Q matrix with potential optimizations
    for i, q in enumerate(Q):
        q = utils.promote(q)
        if q.dim() <= 1:
            # Scalar case - use in-place division
            conjB.div_(q)
        else:
            # Matrix case - use optimized triangular solve
            # Reshape once and contiguous to optimize memory access
            conjB_reshaped = conjB.reshape(-1, q.size(0)).contiguous()
            solved = torch.linalg.solve_triangular(q, conjB_reshaped, upper=True, left=False)
            conjB = solved.reshape_as(conjB)

        # Only transpose if needed for next iteration
        if i < order - 1:
            conjB = conjB.transpose(i, -1)

    return A, conjB


@torch.compile(mode="reduce-overhead")
def psgd_update_precond_core(Q, term1, term2, precond_lr, norm, q):
    """Core computation of psgd_update_precond optimized with torch.compile"""
    term1 *= precond_lr
    if q.dim() < 2:
        term1 *= q / norm.clamp_(min=tiny_bf16)
    else:
        torch.triu(term1, out=term1)
        term1 /= torch.where(norm > 0, utils.psgd_lb(term2, norm), norm).clamp_(tiny_bf16)
        term1 = torch.mm(term1, q)
    return term1


def psgd_update_precond_optimized(Q, exprs, G, precond_lr, oq, store_triu_as_line, V):
    """Optimized version of psgd_update_precond with reduced allocations and torch.compile"""
    exprA, exprGs, _ = exprs

    # Use optimized A and conjB calculation
    A, conjB = psgd_calc_A_and_conjB_optimized(exprA, G, Q, V)

    # Process each Q matrix with optimizations
    for q, exprG, o in zip(Q, exprGs, oq):
        # Use optimized einsum implementations
        term1 = utils.promote(torch.einsum(exprG, A, A))
        term2 = utils.promote(torch.einsum(exprG, conjB, conjB))

        # Compute the update using compiled core function
        term1, term2 = term1 - term2, term1 + term2
        norm = term2.norm(float("inf"))

        try:
            # Try to use the optimized core calculation
            term1 = psgd_update_precond_core(Q, term1, term2, precond_lr, norm, q.to(term1.dtype))
        except (RuntimeError, TypeError):
            # Fallback to original implementation
            term1 *= precond_lr
            if q.dim() < 2:
                term1 *= q.to(term1.dtype) / norm.clamp_(min=tiny_bf16)
            else:
                torch.triu(term1, out=term1)
                term1 /= torch.where(norm > 0, utils.psgd_lb(term2, norm), norm).clamp_(tiny_bf16)
                term1 = torch.mm(term1, q.to(term1.dtype))

        # Convert to line format if needed
        if store_triu_as_line:
            term1 = utils.triu_to_line([term1])[0][1]
            # Apply update directly
            if o.dim() > 0:
                o.add_(term1)
            else:
                o = term1
        else:
            # Apply update directly
            o.add_(term1)


@decorator_knowngood
def psgd_precond_grad_optimized(
    expr: str, ea: Tensor, *preconds: Tensor, caution: bool = False, grad: Optional[Tensor] = None
):
    """Optimized version of psgd_precond_grad with better memory management"""
    if caution:
        ea = utils._compilable_cautioning(grad, ea)

    # Determine minimum dtype once
    md = min_dtype(list(preconds) + [ea])

    # Convert all tensors to the same dtype once
    args = [q.to(md) for q in preconds]
    ea_md = ea.to(md)

    # Optimize the einsum operation by avoiding duplicate conversions
    # and potentially making args contiguous if beneficial
    args_contiguous = [arg.contiguous() if not arg.is_contiguous() else arg for arg in args]
    args_double = args_contiguous + args_contiguous

    # Call einsum once with the combined args list
    new = torch.einsum(expr, *(args_double + [ea_md]))

    # Convert result back to original dtype
    return new.to(ea.dtype)


@decorator_knowngood
def precond_grad_cached_optimized(
    expr: str, ea: Tensor, *cached_q: Tensor, caution: bool = False, grad: Optional[Tensor] = None, cast: bool = True
):
    """Optimized version of precond_grad_cached_ with better memory management"""
    if caution:
        ea = utils._compilable_cautioning(grad, ea)

    # Determine minimum dtype once
    md = min_dtype(list(cached_q) + [ea])

    # Convert all tensors to the same dtype once and make contiguous if needed
    args = [q.to(md).contiguous() if not q.is_contiguous() else q.to(md) for q in cached_q]
    ea_md = ea.to(md).contiguous() if not ea.is_contiguous() else ea.to(md)

    # Add ea_md to args
    args.append(ea_md)

    # Call einsum once with the optimized args
    new = torch.einsum(expr, *args)

    # Convert result back if needed
    if cast:
        return new.to(ea.dtype)
    return new
