# New Candidate Bug Report

Updated: 2026-06-14

This report is intentionally separate from `accepted_bug_report.md` and `accepted_bug_inventory.csv`.
The earlier alias / invalid-input candidates were reviewed by the senior student and should not be mixed into this new count.

## Current Count

| bucket | root-cause families | log/testcase count | conclusion |
|---|---:|---:|---|
| Newly accepted candidates | 1 | RNNBase first 20 all share the same assertion; CUDA repro repeated 3 times | Keep for senior review |
| Pending candidates | 1 | 3 `fractional_max_pool3d` logs | Needs independent CPU/CUDA repro |
| P1 non-RNNBase rejected/noise | 0 accepted | 11 logs | Tool crash, OOM, syntax/generated-code issues |
| P2 first batch rejected/noise | 0 accepted | 53 logs | Comparator limitations, no problem found, random behavior, syntax |

Counting rule: multiple generated programs are counted as one candidate if they share the same root cause.

## N1-001: cuDNN RNN `flatten_parameters` Internal Assert

**Status:** accepted candidate, pending senior judgment.

**Primary API:** `torch.nn.LSTM.flatten_parameters`, traced under `torch.nn.RNNBase`.

**Representative generated source:**

```text
Results/torch/valid/torch.nn.RNNBase_1117.py
```

**Minimal repro:**

```text
repros/pytorch/rnnbase_flatten_internal_assert/repro_lstm_bidirectional_flatten.py
```

**Evidence logs:**

```text
logs/trace_logic_review/repro_logs/p1_txt/rnnbase_cpu.txt
logs/trace_logic_review/repro_logs/p1_txt/rnnbase_cuda.txt
logs/trace_logic_review/repro_logs/p1_txt/rnnbase_cuda_3runs.txt
```

**Observed behavior:**

CPU:

```text
before bidirectional: False
flat_weights: 4
after bidirectional: True
flat_weights: 4
flatten ok
```

CUDA:

```text
RuntimeError: params_from.size(0) == params_to.size(0) INTERNAL ASSERT FAILED
at "/pytorch/aten/src/ATen/native/cudnn/RNN.cpp":1011,
please report a bug to PyTorch. number of layers mismatch
```

CUDA reproduced the same failure in 3 out of 3 runs.

**Root-cause pattern:**

```python
lstm = torch.nn.LSTM(10, 20, batch_first=True, num_layers=1, device="cuda:0")
lstm.bidirectional = True
lstm.flatten_parameters()
```

The module is constructed as a one-direction LSTM, then `bidirectional` is manually mutated to `True`.
That leaves the module metadata inconsistent with the existing flat weight list.
The CUDA/cuDNN path hits an internal assertion instead of raising a normal Python-facing error.

**Caveat:**

This is not a clean normal-user workflow because it mutates an internal configuration attribute after construction.
However, the presence of `INTERNAL ASSERT FAILED` and `please report a bug to PyTorch` makes it worth senior review.

## P1 Non-RNNBase Review

The P1 non-RNNBase batch did not produce new accepted candidates.

Summary:

| group | count | reason |
|---|---:|---|
| TitanFuzz driver/tool crash | 6 | `FrameworkCrashCatch '... has no attribute pre'` |
| CUDA OOM | 2 | `ReplicationPad3d` cases allocate too much memory |
| Generated syntax error | 2 | `Directory`, `PackageImporter` |
| Generated-code/environment issue | 1 | `pixel_unshuffle` source has undefined `device` |

## P2 First Batch Review

No new accepted candidate was added from the first P2 batch.

### P2 `gpu_exec_or_cuda_assert_mismatch`

| result | count | files / notes |
|---|---:|---|
| Pending | 3 | `torch.nn.functional.fractional_max_pool3d_{584,590,614}` produce CUDA `invalid argument` |
| Rejected/no problem | 11 | `FrameworkSingle DuelFailed 420 No problem found` |
| Rejected/random | 2 | `bernoulli_`, `gumbel_softmax` produce `InternalRandomFail` |

The `fractional_max_pool3d` cases are not accepted yet because they still depend on `torch2cuda.py --mode duel`.
They need independent CPU and CUDA repro scripts.

### P2 `final_output_inconsistency` First 40

| result | count | reason |
|---|---:|---|
| Rejected/tool comparator limitation | 27 | `dequantize` candidates fail because `isclose` is unsupported for quantized inputs |
| Rejected/tool comparator limitation | 12 | sparse candidates fail because `aten::eq.Tensor` is unsupported for `SparseCPU` |
| Rejected/generated syntax error | 1 | `torch.Tensor.transpose__157` |

These are not evidence of actual CPU/CUDA output differences. They show that the TitanFuzz comparison layer cannot compare sparse or quantized tensors directly.

## Next Review Target

Next, independently test the pending `fractional_max_pool3d` family:

```text
Results/torch/valid/torch.nn.functional.fractional_max_pool3d_584.py
Results/torch/valid/torch.nn.functional.fractional_max_pool3d_590.py
Results/torch/valid/torch.nn.functional.fractional_max_pool3d_614.py
```

Acceptance requirement:

1. CPU and CUDA are run in separate Python processes.
2. The input shapes and `random_samples` shapes are printed.
3. CPU either succeeds or raises a clear Python exception.
4. CUDA consistently raises `AcceleratorError CUDA error: invalid argument`.
5. The repro is reduced to the smallest valid `fractional_max_pool3d` call.
