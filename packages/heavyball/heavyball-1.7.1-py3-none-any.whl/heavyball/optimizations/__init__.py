"""
PSGD optimization module - optimized implementations of PSGD functions
to improve execution speed while maintaining numerical equivalence.
"""

# Import optimized functions
# Import integrator API
from .integrator import (
    enable_optimizations,
    get_optimization_status,
    restore_original_functions,
)
from .optimizations import (
    # LRA optimizations
    low_rank_mm_optimized,
    lra_precond_optimized,
    precond_grad_cached_optimized,
    # KRON optimizations
    psgd_calc_A_and_conjB_optimized,
    psgd_precond_grad_optimized,
    psgd_update_precond_optimized,
    update_lra_precond_optimized,
)

__all__ = [
    # Optimized functions
    "low_rank_mm_optimized",
    "update_lra_precond_optimized",
    "lra_precond_optimized",
    "psgd_calc_A_and_conjB_optimized",
    "psgd_update_precond_optimized",
    "psgd_precond_grad_optimized",
    "precond_grad_cached_optimized",
    # Integrator API
    "enable_optimizations",
    "restore_original_functions",
    "get_optimization_status",
]
