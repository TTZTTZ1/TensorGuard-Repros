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
| P2 numeric clean rejected/noise | 0 accepted | 60 logs | `eigh`/`svd` vector sign or basis ambiguity, plus 2 generated syntax errors |
| P2 conv/ctc first30 rejected/noise | 0 accepted | 30 logs + independent `conv3d` check | `conv3d` explained by TF32/floating-point tolerance; `ctc_loss` invalid-target cases rejected; `conv_transpose3d` no problem |
| P2 remaining numeric next30 rejected/noise | 0 accepted | 30 logs + source snapshots + FFT deep-dive | FFT differences are expected float32 CPU/GPU numeric variance; `pinverse` divide-by-zero and overflow cases rejected/noise |
| P2 final output balanced51 rejected/noise | 0 accepted | 51 logs + source snapshots | Quantized/sparse outputs hit TitanFuzz comparator limitations; dropout randomness and generated-code errors rejected |
| P2 GPU exec remaining rejected/noise | 0 accepted | 13 logs + source snapshots | 11 reruns report `No problem found`; 2 stochastic APIs report `InternalRandomFail` |
| P2 sparse all rejected/noise | 0 accepted | 1322 logs + source snapshots | 1317 SparseCPU `eq` comparator failures and 5 SparseCsr unsupported-layout comparator failures |
| P2 numeric remaining all rejected/noise | 0 accepted | 119 logs + source snapshots | `svd`/`qr` decomposition ambiguity, disputed `addmm_` alias family, ill-conditioned linear algebra, conv numeric tolerance, and documented `lstsq` driver differences |
| P3 max unpool rejected/noise | 0 accepted | 568 logs + source snapshots | Generated programs use repeated/random/manual indices instead of indices returned by `MaxPool`; PyTorch docs explicitly warn repeated indices may be nondeterministic |

Counting rule: multiple generated programs are counted as one candidate if they share the same root cause.

## Review Evidence Standard

Logs are treated only as an index to suspicious behavior.
A candidate should be added to the accepted/confirmed list only after all of the following are checked:

```text
1. Read the original generated source file under Results/torch.
2. Confirm that the logged failure maps to the actual source behavior.
3. Build or review an independent minimal repro, not only the TitanFuzz-instrumented log.
4. Classify whether the behavior is a framework issue, expected math/library behavior, generated-code bug, or tool-comparator artifact.
```

For future batches, the corresponding source files should be copied or referenced together with the logs so review is not based on logs alone.

## N1-001: cuDNN RNN `flatten_parameters` Internal Assert

**Status:** accepted candidate, pending senior judgment.

**Primary API:** `torch.nn.LSTM.flatten_parameters`, traced under `torch.nn.RNNBase`.

**Representative generated source:**

```text
Results/torch/valid/torch.nn.RNNBase_1117.py
```

**Source review status:** reviewed.
The generated source explicitly mutates `lstm_base.bidirectional = True` after constructing a one-direction LSTM and then calls `lstm_base.flatten_parameters()`.

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

**Source review status:** reviewed.
The representative generated source reshapes `(100, 3, 128, 128)` into `(-1, 4, 4, 4)`, producing `C=76800` for the unbatched 4D fractional max pool input.
That source-level shape explains why the independent reduction focused on the channel boundary around `65536`.

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
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cuda_c65536_3runs.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cuda_5d_c65536_3runs.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cpu_5d_c65535.txt
logs/trace_logic_review/repro_logs/p2_fractional_max_pool3d_txt/cuda_5d_c65535.txt
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

**Repeat and control validation:**

```text
4D C=65536 CUDA repro: failed 3/3 with CUDA error: invalid argument
5D C=65536 CUDA repro: failed 3/3 with CUDA error: invalid argument
5D C=65535 CPU control: ok, y.shape: (1, 65535, 1, 1, 1)
5D C=65535 CUDA control: ok, y.shape: (1, 65535, 1, 1, 1)
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

### P2 `numeric_consistency_check_needed` Clean Batch

No new accepted candidate was added from this batch.

Reviewed logs:

```text
logs/trace_logic_review/repro_logs/p2_numeric_clean_txt/
logs/trace_logic_review/repro_logs/p2_numeric_clean_summary.txt
```

Representative sources reviewed:

```text
Results/torch/valid/torch.linalg.eigh_1056.py
Results/torch/valid/torch.linalg.svd_130.py
```

These sources directly call `torch.linalg.eigh(torch.ones((3, 3)))` and `torch.linalg.svd(A)`.
That matches the log-level conclusion: the observed differences are in decomposition vectors, not in eigenvalues or singular values.

Summary:

| result | count | reason |
|---|---:|---|
| Rejected / expected linear-algebra ambiguity | 47 | `torch.linalg.eigh` differs only in `eigenvectors`; eigenvector signs/bases are not unique |
| Rejected / expected linear-algebra ambiguity | 1 | `torch.linalg.eigh_404` stores eigenvectors in `_`; same sign-choice issue |
| Rejected / expected linear-algebra ambiguity | 10 | `torch.linalg.svd` differs only in `U` and `Vt`; SVD vector signs are not unique |
| Rejected / generated syntax error | 2 | `torch.linalg.eigh_1120` and `torch.linalg.eigh_966` contain an empty `for` block |

Important negative finding:

```text
No reviewed case showed a direct mismatch in eigenvalues or singular values:
- no `diff: ['eigenvalues']`
- no `diff: ['S']`
```

Conclusion:

These logs should not be reported as PyTorch bugs based on raw `VarInconsistentCatch`.
For `eigh` and `svd`, the correct validation should compare invariant properties such as eigenvalues/singular values and matrix reconstruction residuals, not raw eigenvector or singular-vector entries.

### P2 `conv3d` / `conv_transpose3d` / `ctc_loss` First 30

No new accepted candidate was added from this batch.
The `conv3d` root-cause family was independently checked and rejected as a strong bug candidate.

Reviewed logs:

```text
logs/trace_logic_review/repro_logs/p2_conv_ctc_first30_txt/
logs/trace_logic_review/repro_logs/p2_conv_ctc_first30_summary.txt
```

Representative sources reviewed:

```text
Results/torch/valid/torch.nn.functional.conv3d_1.py
Results/torch/valid/torch.nn.functional.conv3d_1028.py
Results/torch/valid/torch.nn.functional.conv3d_1203.py
Results/torch/valid/torch.nn.functional.ctc_loss_222.py
Results/torch/valid/torch.nn.functional.ctc_loss_263.py
```

Summary:

| result | count | source-level conclusion |
|---|---:|---|
| Rejected / expected numeric variance | 10 | `conv3d` sources are normal valid convolution inputs; independent check shows large differences with TF32 enabled but reasonable tolerance when TF32 is disabled |
| Rejected/no problem | 10 | `conv_transpose3d` logs say `FrameworkSingle DuelFailed 420 No problem found` |
| Rejected/invalid generated input | 5 | `ctc_loss` sources use invalid target labels, e.g. `C=1` with targets `[1,2,3,4]`, or `C=4` with target `4` and `blank=1` included in targets |
| Rejected/no problem | 5 | remaining `ctc_loss` logs say `No problem found` |

The `ctc_loss` failures should not be counted as strong PyTorch bugs at this stage.
They are generated invalid-input cases and may exercise undefined or under-validated behavior.

Independent checker:

```text
scripts/check_conv3d_numeric_batch.py
```

Independent result:

```text
logs/trace_logic_review/repro_logs/p2_conv_ctc_first30_txt/conv3d_numeric_independent.txt
```

With TF32 enabled, all `conv3d` cases fail even `allclose(rtol=1e-3, atol=1e-3)`, with max absolute errors around `2.1e-2` to `5.6e-2`.
With TF32 disabled, all cases pass `1e-3`; 9 out of 10 also pass `1e-4`.
The remaining case, `conv3d_1`, has a larger `5x5x5` kernel and still passes `1e-3` with `max_abs=5.0354e-4`.

Conclusion:

These `conv3d` logs are best treated as TF32/cuDNN/CPU floating-point-path differences rather than reportable PyTorch bugs.

### P2 Remaining Numeric Next 30

No new accepted candidate was added from this batch.
The FFT numeric family was independently checked and rejected as a strong bug candidate.

Reviewed logs and source snapshots:

```text
logs/trace_logic_review/repro_logs/p2_remaining_numeric_next30_txt/
logs/trace_logic_review/repro_logs/p2_remaining_numeric_next30_summary.txt
logs/trace_logic_review/source_snapshots/p2_remaining_numeric_next30/
```

Summary:

| result | count | source-level conclusion |
|---|---:|---|
| Rejected / expected numeric variance | 24 | `hfft` / `ihfft` / `ifftn` cases are FFT-heavy legal numeric programs; independent checks show matching finite masks, tiny normalized error, and float64 agreement |
| Rejected/no problem | 2 | `torch.fft.rfft_1032` and `torch.fft.rfft_693` report `No problem found` |
| Rejected / generated numeric overflow | 3 | `rfft_1040`, `rfft_1054`, and `rfft_613` use `cosh` / `sinh` / `exp` on large values, producing `inf` before or around the FFT-relevant result |
| Rejected / divide-by-zero amplification | 1 | `torch.Tensor.pinverse_721` divides pseudo-inverse values by an input tensor containing zero, turning tiny CPU/GPU sign differences into `+inf` versus `-inf` |

Representative source review:

```text
torch.Tensor.pinverse_721.py:
  result = torch.cat((_input_tensor, torch.div(pinverse_result, _input_tensor)), dim=0)
  _input_tensor contains 0.0, so the division is not a clean framework mismatch.

torch.fft.rfft_1040.py / torch.fft.rfft_1054.py:
  y = torch.cosh(...) or torch.sinh(...)
  values overflow to inf, so this is not a clean FFT correctness signal.

torch.fft.ihfft_*:
  repeated fft/ifft/hfft/ihfft chains on float32 complex tensors.
  These are plausible numeric-difference cases but need tolerance and finite-mask checks.
```

Independent checker added:

```text
scripts/check_fft_numeric_batch.py
```

Independent check result:

```text
logs/trace_logic_review/repro_logs/p2_remaining_numeric_next30_txt/fft_numeric_independent.txt
```

Findings:

```text
All representative cases have matching finite masks.
torch.fft.ifftn_1255 passes 1e-5.
torch.fft.ihfft_1059 and torch.fft.ihfft_1400 pass 1e-2.
The remaining loose-tolerance failures are:
  torch.fft.hfft_570
  torch.fft.hfft_779
  torch.fft.hfft_782
  torch.fft.ihfft_1268
  torch.fft.ihfft_773
```

Deep-dive checker:

```text
scripts/check_fft_numeric_deep_dive.py
```

Deep-dive result:

```text
logs/trace_logic_review/repro_logs/p2_remaining_numeric_next30_txt/fft_numeric_deep_dive.txt
```

Findings:

```text
The five loose-tolerance failures all have matching finite masks.
For float32, pointwise absolute errors are visible but L2 relative error is around 1e-7:
  hfft_570:   l2_rel=4.94e-7
  hfft_779:   l2_rel=4.69e-7
  hfft_782:   l2_rel=4.69e-7
  ihfft_1268: l2_rel=9.10e-7
  ihfft_773:  l2_rel=1.44e-7
For float64, all five cases pass 1e-5 and have L2 relative error around 1e-15.
```

Conclusion:

These FFT cases are best treated as expected CPU/GPU float32 numerical variance, not reportable PyTorch bugs.

### P2 Final Output Balanced 51

No new accepted candidate was added from this batch.
The batch is useful because it shows that many `final_output_inconsistency` entries are not real output mismatches; they are unsupported comparison paths in the TitanFuzz checker.

Reviewed logs and source snapshots:

```text
logs/trace_logic_review/repro_logs/p2_final_output_balanced60_txt/
logs/trace_logic_review/repro_logs/p2_final_output_balanced60_summary.txt
logs/trace_logic_review/source_snapshots/p2_final_output_balanced60/
```

Summary:

| result | count | source-level conclusion |
|---|---:|---|
| Rejected / quantized comparator limitation | 32 | `torch.quantize_per_tensor`, `torch.quantize_per_channel`, `torch.quantized_max_pool2d`, and `torch.dequantize` logs fail with `isclose is not supported for quantized inputs`; representative sources produce quantized tensors and the failure is in the comparison path |
| Rejected / sparse comparator limitation | 10 | `torch.hspmm`, `torch.zeros`, and `CorrCholeskyTransform` cases fail because TitanFuzz attempts `aten::eq.Tensor` on `SparseCPU`; representative sources create sparse outputs or convert outputs to sparse |
| Rejected / generated-code or tool issue | 3 | `torch.overrides.get_overridable_functions` cases either report `No problem found`, fail with generated invalid attribute mutation, or fail with comparator type errors |
| Rejected / random behavior | 1 | `torch.nn.functional.dropout3d_619` reports `InternalRandomFail`; source uses dropout in training mode without deterministic seeding for the stochastic mask |
| Rejected / no problem | 5 | `torch.overrides.get_overridable_functions` entries report `No problem found` |

Representative source review:

```text
torch.quantize_per_tensor_1.py:
  quantized_data = torch.quantize_per_tensor(input_data, scale, zero_point, dtype)
  The logged failure is "isclose is not supported for quantized inputs", so this is a checker issue.

torch.hspmm_1.py:
  mat1 = torch.sparse_coo_tensor(...)
  result = torch.hspmm(mat1, mat2)
  The logged failure is "aten::eq.Tensor" unsupported for SparseCPU, so this is a checker issue.

torch.nn.functional.dropout3d_619.py:
  output = torch.nn.functional.dropout3d(output_tensor, 0.5)
  The output is stochastic; the log reports InternalRandomFail, not a clean framework bug.
```

Conclusion:

This batch should not be counted as PyTorch bugs.
Future final-output review should either skip quantized/sparse outputs or use a semantic comparator first:

```text
quantized: compare int_repr(), q_scale(), q_zero_point(), qscheme(), dtype, and dequantized values when appropriate
sparse: compare layout, indices, values, size, coalesced state, and dense result only when invariants are valid
```

### P2 GPU Exec Remaining 13

No new accepted candidate was added from this batch.
This batch closes the remaining `gpu_exec_or_cuda_assert_mismatch` API families after excluding the already accepted `fractional_max_pool3d` family.

Reviewed logs and source snapshots:

```text
logs/trace_logic_review/repro_logs/p2_gpu_exec_remaining_txt/
logs/trace_logic_review/repro_logs/p2_gpu_exec_remaining_summary.txt
logs/trace_logic_review/source_snapshots/p2_gpu_exec_remaining/
```

Summary:

| result | count | source-level conclusion |
|---|---:|---|
| Rejected / no problem on rerun | 11 | `LongStorage`, `nanquantile`, `new_full`, `broadcast_shapes`, `index_select`, `lu`, `binary_cross_entropy`, `pack_padded_sequence`, `pack_sequence`, `take_along_dim`, and `tril_indices` reran with `No problem found` |
| Rejected / random behavior | 2 | `torch.Tensor.bernoulli_` and `torch.nn.functional.gumbel_softmax` report `InternalRandomFail`; sources directly use stochastic sampling |

Representative source review:

```text
torch.Tensor.bernoulli__1470.py:
  y = torch.Tensor.bernoulli_(torch.Tensor.bernoulli_(torch.randn(1)))
  The source nests random sampling and the log reports InternalRandomFail.

torch.nn.functional.gumbel_softmax_326.py:
  logits = logits + torch.randn(*logits.shape) * tau
  output = torch.nn.functional.gumbel_softmax(logits, tau=1.0)
  The source has random noise before a stochastic API, so it is not a clean CPU/GPU bug.
```

Conclusion:

The P2 `gpu_exec_or_cuda_assert_mismatch` category is now fully reviewed by API family.
The only accepted candidate from that category remains `fractional_max_pool3d`.

### P2 Sparse All 1322

No new accepted candidate was added from this batch.
This batch closes the P2 `sparse_logic_inconsistency_caveat` category by API family.

Reviewed logs and source snapshots:

```text
logs/trace_logic_review/queues/p2_sparse_all.txt
logs/trace_logic_review/repro_logs/p2_sparse_all_txt/
logs/trace_logic_review/repro_logs/p2_sparse_all_summary.txt
logs/trace_logic_review/source_snapshots/p2_sparse_all/
```

Summary:

| result | count | source-level conclusion |
|---|---:|---|
| Rejected / SparseCPU comparator limitation | 1317 | `Tensor.to_sparse`, `sparse.addmm`, `sparse.log_softmax`, `sparse.mm`, `sparse.softmax`, `sparse.sum`, and `sparse_coo_tensor` logs fail because TitanFuzz attempts `aten::eq.Tensor` on `SparseCPU`; the failure happens before later sparse operations are meaningfully checked |
| Rejected / SparseCsr comparator limitation | 5 | `sparse_csr_tensor` logs fail with `ComparisonFail unsupported tensor layout: SparseCsr`; the sources create invalid-looking CSR tensors, but the logged failure is still the checker layout path, not a native crash |

API distribution:

```text
torch.Tensor.to_sparse:       206
torch.sparse.addmm:           206
torch.sparse.log_softmax:     225
torch.sparse.mm:               46
torch.sparse.softmax:         204
torch.sparse.sum:             206
torch.sparse_coo_tensor:      224
torch.sparse_csr_tensor:        5
```

Representative source review:

```text
torch.sparse.mm_1.py:
  mat1 = torch.sparse_coo_tensor(...)
  mat2 = torch.sparse_coo_tensor(...)
  _result = torch.sparse.mm(mat1, mat2)
  The log stops at sparse tensor creation because the checker tries SparseCPU equality.

torch.sparse_csr_tensor_1014.py:
  row_indices = torch.arange(4)
  sparse_tensor = torch.sparse_csr_tensor(..., size=(2, 2))
  The later mm operations are present in source, but the log stops at CSR creation with unsupported layout.
```

Conclusion:

This batch should not be counted as PyTorch bugs.
It did not reproduce the earlier strong sparse crashes such as `free(): invalid pointer` or `free(): invalid next size`.
Future sparse review needs a semantic sparse comparator or targeted replay of known crash-like sources, not the generic TitanFuzz equality path.

### P2 Numeric Remaining All 119

No new accepted candidate was added from this batch.
This batch closes the remaining P2 `numeric_consistency_check_needed` queue.

Reviewed logs and source snapshots:

```text
logs/trace_logic_review/queues/p2_numeric_remaining_all.txt
logs/trace_logic_review/repro_logs/p2_numeric_remaining_all_txt/
logs/trace_logic_review/repro_logs/p2_numeric_remaining_all_summary.txt
logs/trace_logic_review/source_snapshots/p2_numeric_remaining_all/
```

Summary:

| result | count | source-level conclusion |
|---|---:|---|
| Rejected / disputed alias and in-place mutation family | 23 | `torch.Tensor.addmm_` sources use in-place matrix multiplication with aliased or overlapping inputs, e.g. `torch.Tensor.addmm_(mat1, mat2, mat1.transpose(0, 1))`; this matches the family already rejected by senior review |
| Rejected / expected linear-algebra ambiguity | 48 | `torch.Tensor.svd` and `torch.svd` differ in `U`, `Vh`, `Vt`, or equivalent vector outputs; singular-vector signs and bases are not unique |
| Rejected / expected linear-algebra ambiguity | 30 | `torch.qr` differs in `Q`-like outputs; QR signs and bases are not unique, especially for rank-deficient products such as `X.T @ X` |
| Rejected / ill-conditioned or singular numeric behavior | 9 | `torch.linalg.cond` sources include singular or near-singular matrices, including duplicated rows; logs show `inf` versus huge finite values or rerun `No problem found` |
| Rejected / invalid numeric setup and amplification | 1 | `torch.linalg.eigvalsh_428` uses non-symmetric input for a Hermitian/eigenvalue API and then applies inverse/divide-by-near-zero operations |
| Rejected / rank-deficient pseudo-inverse variance | 1 | `torch.pinverse_107` computes pseudo-inverse of all-ones rank-deficient tensors; CPU/GPU SVD threshold differences are amplified into huge values |
| Rejected / expected conv numeric tolerance | 5 | `conv2d` and `conv_transpose2d` entries are ordinary float convolution outputs or rerun `No problem found`; based on the previous conv deep-dive, these are treated as numeric tolerance/TF32-path cases unless a no-TF32 check proves otherwise |
| Rejected / documented CPU-CUDA driver behavior | 2 | `torch.linalg.lstsq` CPU and CUDA use different default drivers; PyTorch documentation states CPU defaults to `gelsy`, CUDA defaults to `gels`, and CUDA only supports `gels` assuming full rank |

Representative source review:

```text
torch.Tensor.addmm__1173.py:
  torch.Tensor.addmm_(mat1, mat2, mat1.transpose(0, 1))
  This is the disputed alias/in-place family rather than a clean backend bug.

torch.Tensor.svd_488.py:
  (U, s, Vh) = torch.Tensor.svd(_input_tensor)
  The log diff is `U` and `Vh`, not the singular values.

torch.qr_294.py:
  result = torch.qr(torch.mm(input_data.t(), input_data))[0]
  The log diff is the `Q` basis of a rank-deficient Gram matrix.

torch.linalg.cond_1002.py:
  A has duplicated rows, so the matrix is singular.
  CPU reports `inf`; CUDA reports a huge finite condition number.

torch.linalg.lstsq_552.py:
  solution = torch.linalg.lstsq(A, B, rcond=0.2)[0]
  CPU and CUDA produce different solutions, but this matches documented backend-driver behavior.
```

Conclusion:

This batch should not be counted as PyTorch bugs.
The P2 queue is now fully reviewed by the current staged plan.

### P3 Max Unpool All 568

No new accepted candidate was added from this batch.
This batch closes the P3 `max_unpool_index_semantics` queue.

Reviewed logs and source snapshots:

```text
logs/trace_logic_review/queues/p3_max_unpool_all.txt
logs/trace_logic_review/repro_logs/p3_max_unpool_all_txt/
logs/trace_logic_review/repro_logs/p3_max_unpool_all_summary.txt
logs/trace_logic_review/source_snapshots/p3_max_unpool_all/
```

Summary:

| result | count | source-level conclusion |
|---|---:|---|
| Rejected / repeated `argmax` indices | 561 | Sources construct `indices` with `torch.argmax(...)`, often followed by `expand` or `expand_as`; these are not the indices returned by the matching `MaxPool` operation and contain many repeated target indices |
| Rejected / random indices | 6 | Sources construct `indices` with `torch.randint(...)`, so repeated or semantically unrelated target indices are expected |
| Rejected / manual repeated indices | 1 | `torch.nn.functional.max_unpool1d_seed1.py` uses `indices = torch.tensor([[[1, 1, 1, 1, 1, 1]]])`, forcing all values to the same output position |

API distribution:

```text
torch.nn.functional.max_unpool1d: 232
torch.nn.MaxUnpool3d:             225
torch.nn.functional.max_unpool3d:  76
torch.nn.MaxUnpool2d:              30
torch.nn.functional.max_unpool2d:   5
```

Representative source review:

```text
torch.nn.MaxUnpool2d_1016.py:
  indices = torch.argmax(input_tensor, dim=1, keepdim=True)
  The tensor has one channel, so indices are all zero.
  Many input elements write to the same output index.

torch.nn.functional.max_unpool1d_972.py:
  indices = torch.argmax(input, dim=2, keepdim=True).expand((-1), (-1), input.size(2))
  Each channel repeats one argmax index across the whole length.

torch.nn.functional.max_unpool3d_1.py:
  indices = torch.argmax(input, dim=1, keepdim=True).expand_as(input)
  Channel-wise argmax is expanded to every channel/spatial position.

torch.nn.MaxUnpool3d_seed11.py:
  indices = torch.randint(0, 2, (1, 1, 4, 4, 4), dtype=torch.long)
  Random indices are not the inverse-pooling indices produced by `MaxPool3d`.
```

PyTorch API semantics:

```text
MaxUnpool takes the output of MaxPool plus the indices of maximal values returned by MaxPool.
The official docs also warn that MaxUnpool may behave nondeterministically when input indices contain repeated values.
```

Conclusion:

This batch should not be counted as PyTorch bugs.
The observed CPU/CUDA differences are explained by generated invalid or nondeterministic `indices`, not a clean backend correctness issue.

## Next Review Target

N1-002 is now clean enough to send to the senior student as a strong boundary candidate.
The next step is the remaining P3 `logic_inconsistency_needs_review` queue.
After closing the max-unpool queue, P3 has 552 source candidates across 76 API families:

```text
logic_inconsistency_needs_review: 552 sources, 76 API families
```

Highest-count APIs in the remaining P3 queue:

```text
torch.Tensor.bool:             129
torch.Tensor.sgn_:              93
torch.get_num_interop_threads:  61
torch.nn.BatchNorm3d:           45
torch.Tensor.sub_:              24
torch.Tensor.transpose:         23
torch.set_num_threads:          19
torch.Tensor.argsort:           15
torch.Tensor.corrcoef:          13
torch.Tensor.flipud:            13
```

Review rule for P3:

```text
Do not accept a case only because TitanFuzz reports VarInconsistentCatch.
Read the generated source, rerun the source, and decide whether the difference is:
  1. real framework behavior,
  2. expected API semantics,
  3. random/generated-code noise,
  4. or TitanFuzz comparator/instrumentation artifact.
```
