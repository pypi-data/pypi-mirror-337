"""
Integration module to selectively enable optimized implementations
of PSGD functions while maintaining API compatibility.
"""

import os
import sys
from typing import Any, Dict

import torch

from . import optimizations
from .. import utils

# Store original function references
_original_functions = {}
_optimized_functions = {}

# Mapping of original functions to their optimized versions
OPTIMIZATION_MAP = {
    # LRA functions
    utils.update_lra_precond_: optimizations.update_lra_precond_optimized,
    utils.lra_precond: optimizations.lra_precond_optimized,
    # KRON functions
    utils.psgd_update_precond: optimizations.psgd_update_precond_optimized,
    utils.psgd_precond_grad: optimizations.psgd_precond_grad_optimized,
    utils.precond_grad_cached_: optimizations.precond_grad_cached_optimized,
}

# Config for enabling/disabling optimizations
_config = {
    "enabled": os.environ.get("HEAVYBALL_OPTIMIZE", "1") == "1",
    "torch_compile_allowed": os.environ.get("HEAVYBALL_USE_COMPILE", "1") == "1",
    "enable_lra": True,
    "enable_kron": True,
    "verbose": os.environ.get("HEAVYBALL_VERBOSE", "0") == "1",
}


def _apply_monkey_patch(original_func, optimized_func):
    """Monkey patch a function with its optimized version."""
    if original_func not in _original_functions:
        _original_functions[original_func] = original_func

    # Store reference to the optimized function
    _optimized_functions[original_func] = optimized_func

    # Get the module where the original function is defined
    module = original_func.__module__
    func_name = original_func.__name__

    # Replace the function in its module
    if hasattr(sys.modules[module], func_name):
        setattr(sys.modules[module], func_name, optimized_func)

        if _config["verbose"]:
            print(f"Replaced {module}.{func_name} with optimized version")
    else:
        if _config["verbose"]:
            print(f"Warning: Could not find {func_name} in module {module}")


def enable_optimizations(
    enable: bool = True, lra: bool = True, kron: bool = True, torch_compile: bool = True, verbose: bool = False
):
    """
    Enable or disable PSGD optimizations.

    Args:
        enable: Whether to enable optimizations at all
        lra: Whether to enable LRA-specific optimizations
        kron: Whether to enable Kron-specific optimizations
        torch_compile: Whether to allow torch.compile optimizations
        verbose: Whether to print optimization status messages
    """
    _config["enabled"] = enable
    _config["enable_lra"] = lra
    _config["enable_kron"] = kron
    _config["torch_compile_allowed"] = torch_compile
    _config["verbose"] = verbose

    if verbose:
        print(f"PSGD Optimizations: {'enabled' if enable else 'disabled'}")
        print(f"  - LRA optimizations: {'enabled' if lra else 'disabled'}")
        print(f"  - KRON optimizations: {'enabled' if kron else 'disabled'}")
        print(f"  - torch.compile: {'allowed' if torch_compile else 'disabled'}")

    if not enable:
        # Restore original functions
        restore_original_functions()
        return

    # Apply optimizations based on config
    for orig_func, opt_func in OPTIMIZATION_MAP.items():
        # Skip LRA functions if disabled
        if not _config["enable_lra"] and orig_func in [utils.update_lra_precond_, utils.lra_precond]:
            continue

        # Skip KRON functions if disabled
        if not _config["enable_kron"] and orig_func in [
            utils.psgd_update_precond,
            utils.psgd_precond_grad,
            utils.precond_grad_cached_,
        ]:
            continue

        _apply_monkey_patch(orig_func, opt_func)

    # Disable torch.compile if not allowed
    if not _config["torch_compile_allowed"]:
        # Monkey patch torch.compile to be a no-op
        def _noop_compile(fn, **kwargs):
            return fn

        if not hasattr(torch, "_original_compile"):
            torch._original_compile = torch.compile
            torch.compile = _noop_compile
            if verbose:
                print("Disabled torch.compile (replaced with no-op)")
    else:
        # Restore original torch.compile
        if hasattr(torch, "_original_compile"):
            torch.compile = torch._original_compile
            del torch._original_compile
            if verbose:
                print("Restored original torch.compile")


def restore_original_functions():
    """Restore all original function implementations."""
    for orig_func, func_ref in _original_functions.items():
        module = orig_func.__module__
        func_name = orig_func.__name__

        if hasattr(sys.modules[module], func_name):
            setattr(sys.modules[module], func_name, func_ref)

            if _config["verbose"]:
                print(f"Restored original implementation of {module}.{func_name}")

    # Also restore torch.compile if it was modified
    if hasattr(torch, "_original_compile"):
        torch.compile = torch._original_compile
        del torch._original_compile
        if _config["verbose"]:
            print("Restored original torch.compile")


def get_optimization_status() -> Dict[str, Any]:
    """Get current optimization status."""
    return {
        "enabled": _config["enabled"],
        "lra_enabled": _config["enable_lra"],
        "kron_enabled": _config["enable_kron"],
        "torch_compile_allowed": _config["torch_compile_allowed"],
        "optimized_functions": list(_optimized_functions.keys()),
        "original_functions": list(_original_functions.keys()),
    }


# Auto-initialize optimizations based on environment
if os.environ.get("HEAVYBALL_AUTO_OPTIMIZE", "1") == "1":
    enable_optimizations(
        enable=_config["enabled"],
        lra=_config["enable_lra"],
        kron=_config["enable_kron"],
        torch_compile=_config["torch_compile_allowed"],
        verbose=_config["verbose"],
    )
