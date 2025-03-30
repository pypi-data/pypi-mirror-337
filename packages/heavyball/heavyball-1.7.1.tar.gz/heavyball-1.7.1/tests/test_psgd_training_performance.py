"""
Test PSGD optimizations in a realistic training scenario.
Compare training speed and final model performance between original and optimized implementations.
"""

import os
import sys
import time
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
import torch

# Add parent directory to path to import heavyball
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from heavyball import PSGD, PSGD_LRA
from heavyball.psgd_optimized import enable_optimizations, enable_torch_compile


class MLP(torch.nn.Module):
    """Simple MLP model for testing."""

    def __init__(self, input_dim=784, hidden_dim=256, output_dim=10):
        super().__init__()
        self.fc1 = torch.nn.Linear(input_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = torch.nn.Linear(hidden_dim, output_dim)
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def load_mnist(batch_size=128):
    """Load a small subset of MNIST for testing."""
    # Generate synthetic data if MNIST is not available
    train_x = torch.randn(1000, 784)
    train_y = torch.randint(0, 10, (1000,))

    test_x = torch.randn(200, 784)
    test_y = torch.randint(0, 10, (200,))

    train_dataset = torch.utils.data.TensorDataset(train_x, train_y)
    test_dataset = torch.utils.data.TensorDataset(test_x, test_y)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader


def train_model(model, optimizer, train_loader, epochs=3):
    """Train a model and return losses and time per epoch."""
    model.train()
    criterion = torch.nn.CrossEntropyLoss()

    losses = []
    times = []

    for epoch in range(epochs):
        start_time = time.time()
        epoch_loss = 0.0
        num_batches = 0

        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            num_batches += 1

        epoch_time = time.time() - start_time
        avg_loss = epoch_loss / num_batches

        losses.append(avg_loss)
        times.append(epoch_time)

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}, Time: {epoch_time:.4f}s")

    return losses, times


def evaluate_model(model, test_loader):
    """Evaluate a model and return accuracy."""
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, targets in test_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += targets.size(0)
            correct += (predicted == targets).sum().item()

    accuracy = 100 * correct / total
    return accuracy


def compare_training_performance(optimizer_type="PSGD", use_torch_compile=False):
    """
    Compare training performance between original and optimized PSGD implementations.

    Args:
        optimizer_type: 'PSGD' or 'PSGD_LRA'
        use_torch_compile: Whether to use torch.compile
    """
    print(f"\nComparing training performance for {optimizer_type}")
    print("================================================")

    # Set random seed for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)

    # Load data
    train_loader, test_loader = load_mnist()

    # Create models
    model_orig = MLP()
    model_opt = deepcopy(model_orig)

    # Create optimizers
    lr = 0.01
    if optimizer_type == "PSGD":
        optimizer_cls = PSGD
    else:
        optimizer_cls = PSGD_LRA

    # Disable optimizations for original
    enable_optimizations(False)
    optimizer_orig = optimizer_cls(model_orig.parameters(), lr=lr)

    # Enable optimizations for optimized
    enable_optimizations(True)
    if use_torch_compile and hasattr(torch, "compile"):
        enable_torch_compile()
        print("Using torch.compile for optimized version")

    optimizer_opt = optimizer_cls(model_opt.parameters(), lr=lr)

    # Train and evaluate original model
    print("\nTraining with original implementation:")
    orig_losses, orig_times = train_model(model_orig, optimizer_orig, train_loader)
    orig_accuracy = evaluate_model(model_orig, test_loader)
    print(f"Test accuracy: {orig_accuracy:.2f}%")

    # Train and evaluate optimized model
    print("\nTraining with optimized implementation:")
    opt_losses, opt_times = train_model(model_opt, optimizer_opt, train_loader)
    opt_accuracy = evaluate_model(model_opt, test_loader)
    print(f"Test accuracy: {opt_accuracy:.2f}%")

    # Calculate total times and speedup
    total_orig_time = sum(orig_times)
    total_opt_time = sum(opt_times)
    speedup = total_orig_time / total_opt_time

    print(f"\nTotal time (original): {total_orig_time:.4f}s")
    print(f"Total time (optimized): {total_opt_time:.4f}s")
    print(f"Overall speedup: {speedup:.2f}x")

    # Check if results are equivalent
    loss_diff = abs(orig_losses[-1] - opt_losses[-1])
    acc_diff = abs(orig_accuracy - opt_accuracy)

    print(f"Final loss difference: {loss_diff:.6f}")
    print(f"Accuracy difference: {acc_diff:.2f}%")

    if loss_diff < 1e-3 and acc_diff < 1.0:
        print("Results are equivalent ✓")
    else:
        print("Warning: Results differ!")

    # Plot training curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    epochs = range(1, len(orig_losses) + 1)

    # Plot losses
    ax1.plot(epochs, orig_losses, "bo-", label="Original")
    ax1.plot(epochs, opt_losses, "ro-", label="Optimized")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.set_title("Training Loss")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot times
    ax2.plot(epochs, orig_times, "bo-", label="Original")
    ax2.plot(epochs, opt_times, "ro-", label="Optimized")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Time (seconds)")
    ax2.set_title("Training Time per Epoch")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    fig.suptitle(f"{optimizer_type} Training Performance" + (" with torch.compile" if use_torch_compile else ""))
    plt.tight_layout()

    # Save plot
    filename = f"{optimizer_type.lower()}_training_performance"
    if use_torch_compile:
        filename += "_with_compile"
    filename += ".png"

    plt.savefig(filename)
    print(f"Performance visualization saved to '{filename}'")

    return {
        "orig_losses": orig_losses,
        "opt_losses": opt_losses,
        "orig_times": orig_times,
        "opt_times": opt_times,
        "orig_accuracy": orig_accuracy,
        "opt_accuracy": opt_accuracy,
        "speedup": speedup,
    }


def run_all_comparisons():
    """Run all performance comparisons."""
    results = {}

    # Test PSGD
    results["psgd"] = compare_training_performance("PSGD")

    # Test PSGD_LRA
    results["psgd_lra"] = compare_training_performance("PSGD_LRA")

    # Test with torch.compile if available
    if hasattr(torch, "compile"):
        results["psgd_compile"] = compare_training_performance("PSGD", use_torch_compile=True)
        results["psgd_lra_compile"] = compare_training_performance("PSGD_LRA", use_torch_compile=True)

    # Print summary
    print("\nPerformance Summary")
    print("==================")
    for name, result in results.items():
        print(f"{name}: {result['speedup']:.2f}x speedup")

    return results


if __name__ == "__main__":
    run_all_comparisons()
