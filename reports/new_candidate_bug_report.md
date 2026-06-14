# New Candidate Bug Report

Updated: 2026-06-14

This report is intentionally separate from `accepted_bug_report.md` and `accepted_bug_inventory.csv`.
The earlier alias / invalid-input candidates were reviewed by the senior student and should not be mixed into this new count.

## Current Count

| bucket | root-cause families | log/testcase count | conclusion |
|---|---:|---:|---|
| Newly accepted / confirmed candidates | 2 | RNNBase first 20 share one assertion; `fractional_max_pool3d` CUDA failure reproduced 3 times and sweep found boundary at `C=65536` | Keep for senior review |
| Pending candidates | 0 | - | - |
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

## N1-002: `fractional_max_pool3d` CPU Succeeds But CUDA Raises Invalid Argument

**Status:** confirmed boundary candidate.

**Primary API:** `torch.nn.functional.fractional_max_pool3d`.

**Representative generated sources:**

```text
Results/torch/valid/torch.nn.functional.fractional_max_pool3d_584.py
Results/torch/valid/torch.nn.functional.fractional_max_pool3d_590.py
Results/torch/valid/torch.nn.functional.fractional_max_pool3d_614.py
```

**Independent repro:**

```text
repros/pytorch/fractional_max_pool3d_invalid_argument/repro_fractional_max_pool3d_584.py
repros/pytorch/fractional_max_pool3d_invalid_argument/repro_fractional_max_pool3d_c65536.py
repros/pytorch/fractional_max_pool3d_invalid_argument/repro_fractional_max_pool3d_5d_c65536.py
```

**Evidence logs:**

```text
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cpu_584.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cuda_584.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cuda_584_3runs.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/sweep_cpu.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/sweep_cuda.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cpu_c65536.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cuda_c65536.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cpu_5d_c65536.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cuda_5d_c65536.txt
```

**Observed behavior:**

CPU:

```text
device: cpu
x.shape: (76800, 4, 4, 4)
random_samples.shape: (76800, 4, 4, 4)
ok
y.shape: (76800, 1, 1, 1)
```

CUDA:

```text
device: cuda:0
x.shape: (76800, 4, 4, 4)
random_samples.shape: (76800, 4, 4, 4)
torch.AcceleratorError: CUDA error: invalid argument
```

CUDA reproduced the same failure in 3 out of 3 runs.

**Boundary sweep:**

CPU succeeds for every tested channel count:

```text
C=1, 8, 64, 512, 4096, 16384, 32768, 65535, 65536, 70000, 76800
```

CUDA succeeds through `C=65535`, then fails at `C=65536` and above:

```text
C=65535: OK (65535, 1, 1, 1)
C=65536: AcceleratorError: CUDA error: invalid argument
C=70000: AcceleratorError: CUDA error: invalid argument
C=76800: AcceleratorError: CUDA error: invalid argument
```

**Minimal C=65536 repros:**

4D unbatched input:

```text
CPU  x.shape: (65536, 4, 4, 4)       -> ok, y.shape: (65536, 1, 1, 1)
CUDA x.shape: (65536, 4, 4, 4)       -> AcceleratorError: CUDA error: invalid argument
```

5D batched input:

```text
CPU  x.shape: (1, 65536, 4, 4, 4)    -> ok, y.shape: (1, 65536, 1, 1, 1)
CUDA x.shape: (1, 65536, 4, 4, 4)    -> AcceleratorError: CUDA error: invalid argument
```

**Current root-cause hypothesis:**

The failure is strongly tied to the channel dimension crossing `65535`.
CUDA starts failing at `C=65536` for both 4D unbatched input and 5D batched input.
This looks like a CUDA kernel launch/grid-dimension boundary or a missing CUDA-side validation path.
CPU accepts the same shape and computes a result.

**Caveat:**

This candidate is stronger than a `torch2cuda.py` comparison artifact because it was independently reproduced.
However, it uses a very large channel dimension. It should be presented honestly as a boundary-condition CPU/CUDA discrepancy or CUDA error-handling issue, not as a common small-shape model bug.

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
| Confirmed candidate family | 3 source logs, 1 independent repro | `torch.nn.functional.fractional_max_pool3d_{584,590,614}` map to N1-002 |
| Rejected/no problem | 11 | `FrameworkSingle DuelFailed 420 No problem found` |
| Rejected/random | 2 | `bernoulli_`, `gumbel_softmax` produce `InternalRandomFail` |

The `fractional_max_pool3d` cases were independently reproduced after the first P2 batch. They are now tracked as N1-002.

### P2 `final_output_inconsistency` First 40

| result | count | reason |
|---|---:|---|
| Rejected/tool comparator limitation | 27 | `dequantize` candidates fail because `isclose` is unsupported for quantized inputs |
| Rejected/tool comparator limitation | 12 | sparse candidates fail because `aten::eq.Tensor` is unsupported for `SparseCPU` |
| Rejected/generated syntax error | 1 | `torch.Tensor.transpose__157` |

These are not evidence of actual CPU/CUDA output differences. They show that the TitanFuzz comparison layer cannot compare sparse or quantized tensors directly.

## Next Review Target

Next, finish packaging N1-002:

```text
Run 3 repeats for:
1. repro_fractional_max_pool3d_c65536.py cuda:0
2. repro_fractional_max_pool3d_5d_c65536.py cuda:0
```

Optionally test the 5D control case:

```text
x.shape = (1, 65535, 4, 4, 4)
```

If 5D `C=65535` succeeds and 5D `C=65536` fails, N1-002 is clean enough to send to the senior student as a strong boundary candidate.

After that, continue with P2 `numeric_consistency_check_needed`, but skip alias-heavy APIs first.

Suggested next numeric APIs:

```text
torch.nn.functional.conv3d
torch.linalg.svd
torch.linalg.eigh
torch.nn.functional.ctc_loss
```
