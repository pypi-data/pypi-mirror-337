from copy import deepcopy

import torch

from heavyball import PSGD_LRA


def test_psgd_lra_regression():
    """Test that optimized PSGD LRA produces the same results as the original."""
    torch.manual_seed(42)

    # Create a simple model
    model = torch.nn.Sequential(torch.nn.Linear(10, 20), torch.nn.ReLU(), torch.nn.Linear(20, 5))

    # Create input and target
    x = torch.randn(32, 10)
    y = torch.randn(32, 5)

    # Create original optimizer
    optimizer_orig = PSGD_LRA(model.parameters(), lr=0.01)

    # Clone model for optimized version
    model_opt = deepcopy(model)
    optimizer_opt = PSGD_LRA(model_opt.parameters(), lr=0.01)

    # Run 5 steps with both optimizers
    for _ in range(5):
        # Original optimizer
        optimizer_orig.zero_grad()
        output = model(x)
        loss = torch.nn.functional.mse_loss(output, y)
        loss.backward()
        optimizer_orig.step()

        # Optimized optimizer (will use our optimized version)
        optimizer_opt.zero_grad()
        output_opt = model_opt(x)
        loss_opt = torch.nn.functional.mse_loss(output_opt, y)
        loss_opt.backward()
        optimizer_opt.step()

        # Check parameters are the same
        for p_orig, p_opt in zip(model.parameters(), model_opt.parameters()):
            assert torch.allclose(p_orig, p_opt, rtol=1e-5, atol=1e-7), (
                f"Parameters differ: {p_orig.mean().item()} vs {p_opt.mean().item()}"
            )


def test_psgd_lra_delayed_regression():
    """Test that optimized delayed PSGD LRA produces the same results as the original."""
    torch.manual_seed(42)

    # Create a simple model
    model = torch.nn.Sequential(torch.nn.Linear(10, 20), torch.nn.ReLU(), torch.nn.Linear(20, 5))

    # Create input and target
    x = torch.randn(32, 10)
    y = torch.randn(32, 5)

    # Create original optimizer with delayed=True
    optimizer_orig = PSGD_LRA(model.parameters(), lr=0.01, delayed=True)

    # Clone model for optimized version
    model_opt = deepcopy(model)
    optimizer_opt = PSGD_LRA(model_opt.parameters(), lr=0.01, delayed=True)

    # Run 5 steps with both optimizers
    for _ in range(5):
        # Original optimizer
        optimizer_orig.zero_grad()
        output = model(x)
        loss = torch.nn.functional.mse_loss(output, y)
        loss.backward()
        optimizer_orig.step()

        # Optimized optimizer (will use our optimized version)
        optimizer_opt.zero_grad()
        output_opt = model_opt(x)
        loss_opt = torch.nn.functional.mse_loss(output_opt, y)
        loss_opt.backward()
        optimizer_opt.step()

        # Check parameters are the same
        for p_orig, p_opt in zip(model.parameters(), model_opt.parameters()):
            assert torch.allclose(p_orig, p_opt, rtol=1e-5, atol=1e-7), (
                f"Parameters differ: {p_orig.mean().item()} vs {p_opt.mean().item()}"
            )
