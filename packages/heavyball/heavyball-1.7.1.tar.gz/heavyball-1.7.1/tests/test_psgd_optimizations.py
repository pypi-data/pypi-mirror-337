import torch

from heavyball.utils import (
    low_rank_mm,
    lra_precond,
    update_lra_precond_,
)


def test_low_rank_mm_equivalence():
    """Test that optimized low_rank_mm produces the same output as original."""
    # Setup test inputs
    batch_size = 128
    rank = 16
    U = torch.randn(batch_size, rank)
    V = torch.randn(batch_size, rank)
    x = torch.randn(batch_size)

    # Save original function
    original_low_rank_mm = low_rank_mm

    # Reference output
    with torch.no_grad():
        ref_output = original_low_rank_mm(U, V, x)

    # Evaluate optimized function
    from heavyball.optimized import low_rank_mm_optimized

    with torch.no_grad():
        opt_output = low_rank_mm_optimized(U, V, x)

    assert torch.allclose(ref_output, opt_output, rtol=1e-5, atol=1e-6)


def test_lra_precond_equivalence():
    """Test that optimized lra_precond produces the same output as original."""
    batch_size = 256
    rank = 8
    U = torch.randn(batch_size, rank)
    V = torch.randn(batch_size, rank)
    d = torch.rand(batch_size) + 0.1  # Ensure positive values
    g = torch.randn(batch_size)

    # Reference output
    with torch.no_grad():
        ref_output = lra_precond(U, V, d, g)

    # Evaluate optimized function
    from heavyball.optimized import lra_precond_optimized

    with torch.no_grad():
        opt_output = lra_precond_optimized(U, V, d, g)

    assert torch.allclose(ref_output, opt_output, rtol=1e-5, atol=1e-6)


def test_update_lra_precond_equivalence():
    """Test that optimized update_lra_precond_ produces the same outputs as original."""
    # Setup
    batch_size = 64
    rank = 4

    # Create test inputs
    U_orig = [torch.randn(batch_size, rank)]
    V_orig = [torch.randn(batch_size, rank)]
    d_orig = [torch.rand(batch_size) + 0.1]  # Ensure positive values
    vector = torch.randn(batch_size)
    hessian_vector = torch.randn(batch_size)
    eps = 1e-8
    step = 0.01
    delayed = False

    # Make copies for the original and optimized versions
    U_ref = [u.clone() for u in U_orig]
    V_ref = [v.clone() for v in V_orig]
    d_ref = [d.clone() for d in d_orig]

    U_opt = [u.clone() for u in U_orig]
    V_opt = [v.clone() for v in V_orig]
    d_opt = [d.clone() for d in d_orig]

    # Reference outputs
    with torch.no_grad():
        ref_U, ref_V, ref_d = update_lra_precond_(U_ref, V_ref, d_ref, vector, hessian_vector, eps, step, delayed)

    # Optimized outputs
    from heavyball.optimized import update_lra_precond_optimized

    with torch.no_grad():
        opt_U, opt_V, opt_d = update_lra_precond_optimized(
            U_opt, V_opt, d_opt, vector, hessian_vector, eps, step, delayed
        )

    # Check equivalence
    assert torch.allclose(ref_U, opt_U, rtol=1e-4, atol=1e-5)
    assert torch.allclose(ref_V, opt_V, rtol=1e-4, atol=1e-5)
    assert torch.allclose(ref_d, opt_d, rtol=1e-4, atol=1e-5)
