import pytest
import torch

from heavyball import ForeachPSGDKron
from heavyball.utils import line_to_triu


# Helper function to compare optimizer states, handling line format
def compare_states(state1, state2, store_triu_as_line):
    # Ensure the state dictionaries track the same parameters in the same order
    p_list1 = list(state1.keys())
    p_list2 = list(state2.keys())
    assert len(p_list1) == len(p_list2), "State dictionaries track different numbers of parameters"
    for i, (p1, p2) in enumerate(zip(p_list1, p_list2)):
        # Check if parameters themselves are identical (or at least have same shape/dtype)
        assert p1.shape == p2.shape, f"Parameter shape mismatch at index {i}"
        assert p1.dtype == p2.dtype, f"Parameter dtype mismatch at index {i}"
        # It's okay if they are different objects, as long as they correspond

        s1 = state1[p1]
        s2 = state2[p2]
        for k in s1.keys():
            assert k in s2, f"Key {k} missing in second state for param {p1}"
            v1 = s1[k]
            v2 = s2[k]

            # Determine dtype for tolerance setting (default to float32 if ambiguous)
            current_dtype = torch.float32
            if isinstance(v1, torch.Tensor):
                current_dtype = v1.dtype
            elif isinstance(v1, list) and v1 and isinstance(v1[0], torch.Tensor):
                current_dtype = v1[0].dtype
            elif (
                k == "Q"
                and store_triu_as_line
                and isinstance(v1, list)
                and v1
                and isinstance(v1[0], tuple)
                and isinstance(v1[0][1], torch.Tensor)
            ):
                current_dtype = v1[0][1].dtype  # Infer from tensor part of tuple

            # Set tolerances based on dtype
            rtol = 1e-3 if current_dtype == torch.bfloat16 else 1e-6
            atol = 1e-4 if current_dtype == torch.bfloat16 else 1e-7

            if k == "Q" and store_triu_as_line:
                # Materialize Q from line format for comparison
                q1_mat = line_to_triu(v1)
                q2_mat = v2  # v2 should already be materialized
                assert len(q1_mat) == len(q2_mat), f"Mismatch in Q list length for {k}"
                for q1_item, q2_item in zip(q1_mat, q2_mat):
                    torch.testing.assert_close(q1_item, q2_item, rtol=rtol, atol=atol, msg=f"State mismatch for {k}")
            elif isinstance(v1, torch.Tensor):
                torch.testing.assert_close(v1, v2, rtol=rtol, atol=atol, msg=f"State mismatch for {k}")
            elif isinstance(v1, list) and all(isinstance(i, torch.Tensor) for i in v1):
                assert len(v1) == len(v2), f"Mismatch in list length for {k}"
                for i1, i2 in zip(v1, v2):
                    torch.testing.assert_close(i1, i2, rtol=rtol, atol=atol, msg=f"State mismatch for {k} (list item)")
            else:
                # Non-tensor state comparison
                assert v1 == v2, f"State mismatch for {k}"

    # Check for keys present in s2 but not s1
    for p1 in p_list1:  # Use p_list1 as keys should be consistent now
        s1 = state1[p1]
        s2 = state2[p1]  # Use same param key
        for k in s2.keys():
            assert k in s1, f"Key {k} missing in first state for param {p1}"


@pytest.mark.parametrize("dtype", [torch.float32, torch.bfloat16])
@pytest.mark.parametrize("cached", [False, True])
@pytest.mark.parametrize("delayed", [False, True])
@pytest.mark.parametrize("exp_avg_input", [False, True])
def test_psgd_kron_line_format_consistency(dtype, cached, delayed, exp_avg_input):
    """
    Tests that ForeachPSGDKron with store_triu_as_line=True produces
    identical results and states compared to store_triu_as_line=False
    after the optimization in psgd_update_precond.
    """
    if dtype == torch.bfloat16 and not torch.cuda.is_bf16_supported():
        pytest.skip("BF16 not supported on this device")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Simple model
    model1 = torch.nn.Linear(10, 5, bias=False).to(device, dtype=dtype)
    model2 = torch.nn.Linear(10, 5, bias=False).to(device, dtype=dtype)
    # Ensure initial weights are identical
    with torch.no_grad():
        model2.weight.copy_(model1.weight)

    # Optimizers with identical settings except store_triu_as_line
    common_kwargs = dict(
        lr=1e-3,
        beta=0.9,
        weight_decay=0.0,
        max_size_triangular=64,  # Keep small for testing
        q_dtype=str(dtype).split(".")[-1],  # Convert torch.dtype to string name
        storage_dtype=str(dtype).split(".")[-1],  # Convert torch.dtype to string name
        cached=cached,
        delayed=delayed,
        exp_avg_input=exp_avg_input,
        preconditioner_update_probability=1.0,  # Ensure update happens
    )
    opt1 = ForeachPSGDKron(model1.parameters(), store_triu_as_line=True, **common_kwargs)
    opt2 = ForeachPSGDKron(model2.parameters(), store_triu_as_line=False, **common_kwargs)

    # Dummy input and gradient generation
    input_data = torch.randn(16, 10, device=device, dtype=dtype)

    for step in range(3):
        opt1.zero_grad()
        opt2.zero_grad()

        output1 = model1(input_data)
        output2 = model2(input_data)
        loss1 = output1.mean()
        loss2 = output2.mean()

        loss1.backward()
        loss2.backward()

        # Set tolerances based on dtype
        rtol = 1e-3 if dtype == torch.bfloat16 else 1e-6
        atol = 1e-4 if dtype == torch.bfloat16 else 1e-7

        # Ensure gradients are identical before step
        torch.testing.assert_close(model1.weight.grad, model2.weight.grad, rtol=rtol, atol=atol)

        opt1.step()
        opt2.step()

        # Compare parameters
        torch.testing.assert_close(
            model1.weight, model2.weight, rtol=rtol, atol=atol, msg=f"Weight mismatch at step {step}"
        )

        # Compare optimizer states
        compare_states(opt1.state, opt2.state, store_triu_as_line=True)
