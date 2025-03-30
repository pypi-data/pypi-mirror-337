import torch

from heavyball import utils
from heavyball.utils import lra_precond, psgd_precond_grad, update_lra_precond_


class TestPSGDOptimization:
    def setup_lra_test(self):
        """Setup test data for LRA tests"""
        # Initialize parameters
        torch.manual_seed(42)
        grad = torch.randn(64, 32, requires_grad=True)
        param = [grad.clone()]
        update = [grad.clone()]

        # Create state
        state = {}
        group = {
            "is_preconditioning": True,
            "eps": 1e-8,
            "precond_lr": 0.01,
            "precond_init_scale": 1.0,
            "precond_init_scale_scale": 0.01,
            "rank": 8,
            "q_dtype": "float32",
            "momentum_into_precond_update": False,
        }

        # Initialize LRA components
        U, V, d = utils.init_lra(
            grad,
            group["precond_init_scale"],
            group["precond_init_scale_scale"],
            group["rank"],
            None,
            None,
        )

        return grad, param, update, group, U, V, d

    def setup_kron_test(self):
        """Setup test data for Kron tests"""
        # Initialize parameters
        torch.manual_seed(42)
        grad = torch.randn(64, 32, requires_grad=True)
        param = [grad.clone()]
        update = [grad.clone()]

        # Create state and group
        state = {}
        group = {
            "is_preconditioning": True,
            "eps": 1e-8,
            "precond_lr": 0.01,
            "precond_init_scale": 1.0,
            "precond_init_scale_scale": 0.01,
            "max_size_triangular": 1024,
            "min_ndim_triangular": 2,
            "memory_save_mode": None,
            "q_dtype": "float32",
            "store_triu_as_line": False,
            "momentum_into_precond_update": False,
            "caution": False,
            "weight_decay": 0.0,
            "lr": 0.01,
        }

        # Initialize Kron components
        Q, exprs = utils.init_Q_exprs(
            grad,
            group["precond_init_scale"],
            group["precond_init_scale_scale"],
            group["max_size_triangular"],
            group["min_ndim_triangular"],
            group["memory_save_mode"],
            None,
            None,
        )

        return grad, param, update, group, Q, exprs

    def test_update_lra_precond_consistency(self):
        """Test that optimized update_lra_precond_ produces same results as original"""
        grad, param, update, group, U, V, d = self.setup_lra_test()

        # Clone for original function
        U_orig = [u.clone() for u in U]
        V_orig = [v.clone() for v in V]
        d_orig = [d_.clone() for d_ in d]

        # Clone for optimized function
        U_opt = [u.clone() for u in U]
        V_opt = [v.clone() for v in V]
        d_opt = [d_.clone() for d_ in d]

        # Get random vectors for dampening
        vector, hessian_vector = utils.dampen_grad(grad)

        # Run original function
        u_out, v_out, d_out = update_lra_precond_(
            U_orig, V_orig, d_orig, vector.clone(), hessian_vector.clone(), group["eps"], group["precond_lr"], False
        )

        # Run optimized function
        u_opt_out, v_opt_out, d_opt_out = update_lra_precond_optimized(
            U_opt, V_opt, d_opt, vector.clone(), hessian_vector.clone(), group["eps"], group["precond_lr"], False
        )

        # Check results match
        assert torch.allclose(u_out, u_opt_out, rtol=1e-5, atol=1e-5)
        assert torch.allclose(v_out, v_opt_out, rtol=1e-5, atol=1e-5)
        assert torch.allclose(d_out, d_opt_out, rtol=1e-5, atol=1e-5)

        # Also check the actual states were updated the same way
        for u_orig, u_opt in zip(U_orig, U_opt):
            assert torch.allclose(u_orig, u_opt, rtol=1e-5, atol=1e-5)

        for v_orig, v_opt in zip(V_orig, V_opt):
            assert torch.allclose(v_orig, v_opt, rtol=1e-5, atol=1e-5)

        for d_orig, d_opt in zip(d_orig, d_opt):
            assert torch.allclose(d_orig, d_opt, rtol=1e-5, atol=1e-5)

    def test_lra_precond_consistency(self):
        """Test that optimized lra_precond produces same results as original"""
        grad, param, update, group, U, V, d = self.setup_lra_test()

        # Flatten inputs
        u_flat = utils.flatten(U, 1)
        v_flat = utils.flatten(V, 1)
        d_flat = utils.flatten(d)
        g_flat = utils.flatten(update)

        # Run original function
        result_orig = lra_precond(u_flat, v_flat, d_flat, g_flat)

        # Run optimized function
        result_opt = lra_precond_optimized(u_flat, v_flat, d_flat, g_flat)

        # Check results match
        assert torch.allclose(result_orig, result_opt, rtol=1e-5, atol=1e-5)

    def test_psgd_update_precond_consistency(self):
        """Test that optimized psgd_update_precond produces same results as original"""
        grad, param, update, group, Q, exprs = self.setup_kron_test()

        # Clone for original function
        Q_orig = [q.clone() for q in Q]

        # Clone for optimized function
        Q_opt = [q.clone() for q in Q]

        # Get random vectors for dampening
        vector, hessian_vector = utils.dampen_grad(grad)

        # Run original function
        utils.psgd_update_precond(
            Q_orig, exprs, hessian_vector.clone(), group["precond_lr"], Q_orig, False, vector.clone()
        )

        # Run optimized function
        psgd_update_precond_optimized(
            Q_opt, exprs, hessian_vector.clone(), group["precond_lr"], Q_opt, False, vector.clone()
        )

        # Check results match
        for q_orig, q_opt in zip(Q_orig, Q_opt):
            assert torch.allclose(q_orig, q_opt, rtol=1e-5, atol=1e-5)

    def test_psgd_precond_grad_consistency(self):
        """Test that optimized psgd_precond_grad produces same results as original"""
        grad, param, update, group, Q, exprs = self.setup_kron_test()

        # Run original function
        result_orig = psgd_precond_grad(exprs[-1], update[0], *Q, caution=False, grad=grad)

        # Run optimized function
        result_opt = psgd_precond_grad_optimized(exprs[-1], update[0], *Q, caution=False, grad=grad)

        # Check results match
        assert torch.allclose(result_orig, result_opt, rtol=1e-5, atol=1e-5)


# Import optimized versions (these will be implemented)
from heavyball.optimizations import (
    lra_precond_optimized,
    psgd_precond_grad_optimized,
    psgd_update_precond_optimized,
    update_lra_precond_optimized,
)
