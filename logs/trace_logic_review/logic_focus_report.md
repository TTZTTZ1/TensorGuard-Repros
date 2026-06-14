# Trace Logic Review

- Results dir: `Results/torch`
- Reviewed trace candidates: `26329`
- Focus candidates: `3829`
- Excluded/noise candidates: `22500`

## Catch Counts

| catch | count |
| --- | ---: |
| `BothExecFail` | 487596 |
| `Success` | 244460 |
| `InternalRandomFail` | 11892 |
| `GpuExecFail` | 10348 |
| `ExceptMsgCatch` | 8570 |
| `VarInconsistentCatch` | 4520 |
| `ComparisonFail` | 2591 |
| `TimeoutSkipped` | 2038 |
| `GpuNotImplementedFail` | 1894 |
| `SyntaxFail` | 1773 |
| `ExecStateCatch` | 746 |
| `GpuCrashCatch` | 289 |
| `TimeoutFail` | 126 |
| `RandCheckExecFail` | 105 |
| `VarTypeConflictCatch` | 102 |
| `invalid` | 92 |
| `FrameworkCrashCatch` | 11 |
| `271,` | 1 |

## Focus Categories

| category | count |
| --- | ---: |
| `sparse_logic_inconsistency_caveat` | 1322 |
| `numeric_consistency_check_needed` | 702 |
| `max_unpool_index_semantics` | 568 |
| `logic_inconsistency_needs_review` | 552 |
| `final_output_inconsistency` | 369 |
| `strong_backend_failure` | 300 |
| `gpu_exec_or_cuda_assert_mismatch` | 16 |

## Excluded Categories

| category | count |
| --- | ---: |
| `gpu_exec_regular_exception` | 10171 |
| `exception_message_difference_low_value` | 7089 |
| `generated_code_error` | 1628 |
| `alias_or_mutation_semantics` | 1332 |
| `device_or_metadata_semantics` | 1120 |
| `nan_inf_or_boundary_numeric` | 863 |
| `uninitialized_or_lazy_state` | 207 |
| `tool_or_environment_limit` | 90 |

## Top Logic APIs In Raw Trace

| api | VarInconsistentCatch + ComparisonFail |
| --- | ---: |
| `torch.nn.functional.max_unpool1d` | 242 |
| `torch.sparse_coo_tensor` | 237 |
| `torch.Tensor.get_device` | 235 |
| `torch.nn.parameter.UninitializedBuffer` | 231 |
| `torch.sparse.softmax` | 231 |
| `torch.nn.parameter.UninitializedParameter` | 230 |
| `torch.sparse.log_softmax` | 229 |
| `torch.nn.MaxUnpool3d` | 226 |
| `torch.empty_like` | 223 |
| `torch.nn.functional.conv3d` | 219 |
| `torch.sparse.sum` | 217 |
| `torch.Tensor.is_shared` | 212 |
| `torch.linalg.svd` | 210 |
| `torch.sparse.addmm` | 210 |
| `torch.Tensor.data_ptr` | 209 |
| `torch.Tensor.to_sparse` | 209 |
| `torch.Tensor.size` | 193 |
| `torch.Tensor.bool` | 164 |
| `torch.Tensor.sparse_dim` | 158 |
| `torch.Tensor.pinverse` | 157 |
| `torch.distributions.lkj_cholesky.LKJCholesky` | 154 |
| `torch.det` | 149 |
| `torch.nn.BatchNorm3d` | 141 |
| `torch.Tensor.share_memory_` | 138 |
| `torch.nn.functional.ctc_loss` | 113 |
| `torch.Tensor.ger` | 108 |
| `torch.hspmm` | 104 |
| `torch.special.log1p` | 96 |
| `torch.Tensor.sgn_` | 93 |
| `torch.Tensor.resize_as_` | 88 |
| `torch.Tensor.logdet` | 86 |
| `torch.quantize_per_tensor` | 85 |
| `torch.nn.functional.max_unpool3d` | 77 |
| `torch.quantized_max_pool2d` | 76 |
| `torch.atanh` | 68 |
| `torch.get_num_interop_threads` | 61 |
| `torch.linalg.eigh` | 56 |
| `torch.fft.fft` | 55 |
| `torch.Tensor.amin` | 53 |
| `torch.dequantize` | 51 |

## Top Focus APIs

| api | focus candidates |
| --- | ---: |
| `torch.nn.RNNBase` | 289 |
| `torch.nn.functional.max_unpool1d` | 232 |
| `torch.nn.MaxUnpool3d` | 225 |
| `torch.sparse.log_softmax` | 225 |
| `torch.sparse_coo_tensor` | 224 |
| `torch.Tensor.to_sparse` | 206 |
| `torch.sparse.addmm` | 206 |
| `torch.sparse.sum` | 206 |
| `torch.sparse.softmax` | 204 |
| `torch.nn.functional.conv3d` | 189 |
| `torch.linalg.svd` | 188 |
| `torch.Tensor.bool` | 129 |
| `torch.hspmm` | 104 |
| `torch.Tensor.sgn_` | 93 |
| `torch.nn.functional.ctc_loss` | 83 |
| `torch.quantize_per_tensor` | 79 |
| `torch.nn.functional.max_unpool3d` | 76 |
| `torch.quantized_max_pool2d` | 69 |
| `torch.get_num_interop_threads` | 61 |
| `torch.dequantize` | 50 |
| `torch.linalg.eigh` | 50 |
| `torch.sparse.mm` | 46 |
| `torch.nn.BatchNorm3d` | 45 |
| `torch.nn.functional.conv_transpose3d` | 42 |
| `torch.Tensor.svd` | 36 |
| `torch.quantize_per_channel` | 34 |
| `torch.nn.MaxUnpool2d` | 30 |
| `torch.qr` | 30 |
| `torch.overrides.get_overridable_functions` | 27 |
| `torch.Tensor.sub_` | 24 |
| `torch.Tensor.addmm_` | 23 |
| `torch.Tensor.transpose` | 23 |
| `torch.fft.ihfft` | 19 |
| `torch.set_num_threads` | 19 |
| `torch.Tensor.argsort` | 15 |
| `torch.Tensor.corrcoef` | 13 |
| `torch.Tensor.flipud` | 13 |
| `torch.svd` | 12 |
| `torch.Tensor.reshape_as` | 11 |
| `torch.Tensor.mv` | 10 |
| `torch.Tensor.polygamma_` | 9 |
| `torch.linalg.cond` | 9 |
| `torch.Tensor.tan` | 8 |
| `torch.distributed.barrier` | 6 |
| `torch.fft.rfft` | 6 |
| `torch.Tensor.numel` | 5 |
| `torch.nn.functional.max_unpool2d` | 5 |
| `torch.sparse_csr_tensor` | 5 |
| `torch.fft.hfft` | 4 |
| `torch.nn.functional.conv_transpose2d` | 4 |
| `torch.Tensor.put_` | 3 |
| `torch.nn.functional.fractional_max_pool3d` | 3 |
| `torch.orgqr` | 3 |
| `torch.Tensor.erfinv` | 2 |
| `torch.Tensor.less_` | 2 |
| `torch.linalg.lstsq` | 2 |
| `torch.nn.ModuleDict` | 2 |
| `torch.nn.MultiheadAttention` | 2 |
| `torch.nn.ReplicationPad3d` | 2 |
| `torch.nn.Softmax` | 2 |

## First Focus Candidates By Category

### sparse_logic_inconsistency_caveat

- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1013` source=`Results/torch/valid/torch.Tensor.to_sparse_1013.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.ones(4, 4)) | torch.spmm(input_tensor, output_tensor) | torch.mm(input_tensor, output_tensor) | torch.spmm(input_tensor, output_tensor.t()) | torch.matmul(input_tensor, output_tensor)`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1014` source=`Results/torch/valid/torch.Tensor.to_sparse_1014.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.rand(4, 4)) | torch.mm(input_tensor, output_tensor) | torch.spmm(input_tensor, output_tensor) | torch.mm(input_tensor, output_tensor) | torch.spmm(input_tensor, output_tensor.t()) | torch.matmul(input_tensor, output_tensor)`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1034` source=`Results/torch/valid/torch.Tensor.to_sparse_1034.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.rand(4, 4)) | torch.spmm(input_tensor, output_tensor.t()) | torch.mm(input_tensor, output_tensor) | torch.spmm(input_tensor, output_tensor.t()) | torch.matmul(input_tensor, output_tensor)`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1076` source=`Results/torch/valid/torch.Tensor.to_sparse_1076.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `output_tensor = torch.Tensor.to_sparse(torch.arange(0, 10))`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1077` source=`Results/torch/valid/torch.Tensor.to_sparse_1077.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1084` source=`Results/torch/valid/torch.Tensor.to_sparse_1084.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu'))) | output_tensor = output_tensor.to_dense()`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_11` source=`Results/torch/valid/torch.Tensor.to_sparse_11.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `output_tensor = torch.Tensor.to_sparse(torch.randn(3, 5))`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1102` source=`Results/torch/valid/torch.Tensor.to_sparse_1102.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu'))) | input_tensor.sparse_storage = output_tensor`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1163` source=`Results/torch/valid/torch.Tensor.to_sparse_1163.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.eye(4)) | torch.mm(input_tensor, output_tensor) | torch.spmm(input_tensor, output_tensor.t()) | torch.matmul(input_tensor, output_tensor) | torch.matmul(input_tensor, output_tensor.t())`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1164` source=`Results/torch/valid/torch.Tensor.to_sparse_1164.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.eye(4)) | torch.mm(input_tensor, output_tensor) | torch.spmm(input_tensor, output_tensor.t()) | torch.matmul(input_tensor, output_tensor) | torch.matmul(output_tensor, input_tensor)`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1174` source=`Results/torch/valid/torch.Tensor.to_sparse_1174.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.eye(4)) | torch.mm(input_tensor, output_tensor) | torch.spmm(input_tensor, output_tensor.t()) | torch.matmul(input_tensor, output_tensor) | torch.spmm(output_tensor, input_tensor.t())`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1192` source=`Results/torch/valid/torch.Tensor.to_sparse_1192.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.eye(4)) | torch.mm(input_tensor, output_tensor) | torch.spmm(input_tensor, output_tensor.t()) | torch.matmul(input_tensor, output_tensor) | torch.diagonal(torch.spmm(input_tensor, output_tensor.t()))`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1215` source=`Results/torch/valid/torch.Tensor.to_sparse_1215.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.ones(4, 4)) | input_tensor.zero_() | input_tensor.to('cpu') | output_tensor.to_dense() | output_tensor.to('cpu') | torch.sparse.mm(input_tensor, output_tensor) | torch.mm(input_tensor, output_tensor)`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1222` source=`Results/torch/valid/torch.Tensor.to_sparse_1222.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu'))) | output_tensor`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1224` source=`Results/torch/valid/torch.Tensor.to_sparse_1224.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu'))) | output = torch.spmm(input_tensor, output_tensor)`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1229` source=`Results/torch/valid/torch.Tensor.to_sparse_1229.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu'))) | (output_tensor, input_tensor)`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1234` source=`Results/torch/valid/torch.Tensor.to_sparse_1234.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu'))) | output_tensor = output_tensor.to`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1241` source=`Results/torch/valid/torch.Tensor.to_sparse_1241.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu'))) | result = torch.matmul(output_tensor, input_tensor) | result.device`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1252` source=`Results/torch/valid/torch.Tensor.to_sparse_1252.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu'))) | input_tensor.requires_grad_(True) | output_tensor.requires_grad_(True)`
- `P2` `ComparisonFail` `torch.Tensor.to_sparse` `torch.Tensor.to_sparse_1256` source=`Results/torch/valid/torch.Tensor.to_sparse_1256.py`
  - reason: sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable
  - snippet: `input_tensor = torch.ones(4, 4) | output_tensor = torch.Tensor.to_sparse(torch.FloatTensor(input_tensor)) | torch.mm(input_tensor, output_tensor)`

### numeric_consistency_check_needed

- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1010` source=`Results/torch/valid/torch.Tensor.addmm__1010.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `_input_tensor = torch.zeros(2, 2) | _input_tensor = (_input_tensor + (torch.randn_like(_input_tensor).unsqueeze(dim=0) * 3)) | mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2)) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1016` source=`Results/torch/valid/torch.Tensor.addmm__1016.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `_input_tensor = torch.zeros(2, 2) | _input_tensor = (_input_tensor + (torch.randn_like(_input_tensor).unsqueeze(dim=0) * 3)) | mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2)) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.transpose(0, 1))`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1097` source=`Results/torch/valid/torch.Tensor.addmm__1097.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `_input_tensor = torch.zeros(2, 2) | _input_tensor = (_input_tensor + (torch.randn_like(_input_tensor).unsqueeze(dim=0) * 3)) | mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2)) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1.t(), mat2, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1129` source=`Results/torch/valid/torch.Tensor.addmm__1129.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `_input_tensor = torch.zeros(2, 2) | _input_tensor = (_input_tensor + (torch.randn_like(_input_tensor).unsqueeze(dim=0) * 3)) | mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2)) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.T)`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1167` source=`Results/torch/valid/torch.Tensor.addmm__1167.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `_input_tensor = torch.zeros(2, 2) | _input_tensor = (_input_tensor + (torch.randn_like(_input_tensor).unsqueeze(dim=0) * 3)) | mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2)) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1.t(), mat1, mat2.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1173` source=`Results/torch/valid/torch.Tensor.addmm__1173.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - evidence: `already_reviewed`
  - snippet: `mat1 = torch.FloatTensor([[1.0, 2.0], [3.0, 4.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.transpose(0, 1))`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1195` source=`Results/torch/valid/torch.Tensor.addmm__1195.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `_input_tensor = torch.zeros(2, 2) | _input_tensor = (_input_tensor + (torch.randn_like(_input_tensor).unsqueeze(dim=0) * 3)) | mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2)) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat2, mat1, mat2.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1426` source=`Results/torch/valid/torch.Tensor.addmm__1426.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.tensor([[0.0, 3.0], [4.0, 5.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1434` source=`Results/torch/valid/torch.Tensor.addmm__1434.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.tensor([[1.0, 2.0], [3.4, 5.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat1, mat2.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1439` source=`Results/torch/valid/torch.Tensor.addmm__1439.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.Tensor([[1.0, 2.0], [3.0, 4.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1582` source=`Results/torch/valid/torch.Tensor.addmm__1582.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `_input_tensor = torch.zeros(2, 2) | _input_tensor = (_input_tensor + (torch.randn_like(_input_tensor).unsqueeze(dim=0) * 3)) | mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2)) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1.T, mat2, mat1.T, alpha=1.0).squeeze()`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1706` source=`Results/torch/valid/torch.Tensor.addmm__1706.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `_input_tensor = torch.zeros(2, 2) | _input_tensor = torch.tensor(_input_tensor) | _input_tensor = (_input_tensor + (torch.randn_like(_input_tensor).unsqueeze(dim=0) * 3)) | mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2)) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__1749` source=`Results/torch/valid/torch.Tensor.addmm__1749.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `input_tensor = torch.rand(2, 2) | _input_tensor = input_tensor | mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2)) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.transpose(0, 1))`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__246` source=`Results/torch/valid/torch.Tensor.addmm__246.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.tensor([[2.0, 3.0], [4.0, 5.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__251` source=`Results/torch/valid/torch.Tensor.addmm__251.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.tensor([[10.0, 11.0], [12.0, 13.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__271` source=`Results/torch/valid/torch.Tensor.addmm__271.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.tensor([[0.0, 1.0], [2.0, 3.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__275` source=`Results/torch/valid/torch.Tensor.addmm__275.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.tensor([[1.0, 2.0], [3.0, 0.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1.t(), mat2, torch.transpose(mat1, 0, 1))`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__306` source=`Results/torch/valid/torch.Tensor.addmm__306.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.tensor([[1.0, 2.0], [3.0, 4.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1, mat2, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__31` source=`Results/torch/valid/torch.Tensor.addmm__31.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.tensor([[1.0, 2.0], [3.0, 4.0]]) | torch.Tensor.addmm_(mat1, mat1, mat1.t())`
- `P2` `VarInconsistentCatch` `torch.Tensor.addmm_` `torch.Tensor.addmm__334` source=`Results/torch/valid/torch.Tensor.addmm__334.py`
  - reason: numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting
  - snippet: `mat1 = torch.tensor([[1.0, 2.0], [3.0, 4.0]]) | mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]]) | torch.Tensor.addmm_(mat1.t(), mat1, mat2.t())`

### max_unpool_index_semantics

- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1016` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1016.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2) | output = max_unpool(input_tensor, indices) | output = output.cpu()`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1018` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1018.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2) | output = max_unpool(input_tensor, indices) | output = output[(0, indices, indices, indices)]`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1040` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1040.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2) | output = max_unpool(input_tensor, indices) | output = torch.nn.functional.unfold(output, 2, 2)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1048` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1048.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2) | output = max_unpool(input_tensor, indices) | output = torch.mean(output, dim=1)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1051` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1051.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2) | output = max_unpool(input_tensor, indices) | output = output.squeeze()`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1073` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1073.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2) | output = max_unpool(input_tensor, indices) | output = torch.nn.functional.unfold(output, 2, 2) | output = max_unpool(input_tensor, indices) | output = torch.nn.functional.unfold(output, 2, 2)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1082` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1082.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2) | output = max_unpool(input_tensor, indices) | output = torch.nn.functional.unfold(output, 2, 2) | max_unpool`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1087` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1087.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2) | output = max_unpool(input_tensor, indices) | output = torch.nn.functional.unfold(output, 2, 2) | output = max_unpool(input_tensor, indices)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1096` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1096.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2) | output = max_unpool(input_tensor, indices) | output = torch.nn.functional.unfold(output, 2, 2) | output = torch.nn.functional.unfold(output, 2, 2)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1100` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1100.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = max_unpool(input_tensor, indices)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1101` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1101.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | max_unpool_output = max_unpool(input_tensor, indices)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1102` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1102.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | pool_out = max_unpool(input_tensor, indices) | pool_indices = torch.argmax(pool_out, dim=1)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1104` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1104.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | input_tensor = max_unpool(input_tensor, indices)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1105` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1105.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | outputs = max_unpool(input_tensor, indices)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1106` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1106.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | max_unpool = max_unpool(input_tensor, indices)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1109` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1109.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output_tensor = max_unpool(input_tensor, indices)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1115` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1115.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output_tensor = max_unpool(input_tensor, indices) | (output_tensor.transpose_(2, 1).shape, indices.shape)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1117` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1117.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output_value = max_unpool(input_tensor, indices)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1119` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1119.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | output = max_unpool(input_tensor, indices=indices)`
- `P3` `VarInconsistentCatch` `torch.nn.MaxUnpool2d` `torch.nn.MaxUnpool2d_1120` source=`Results/torch/valid/torch.nn.MaxUnpool2d_1120.py`
  - reason: max_unpool index semantics need manual validation; keep as lower-priority trace candidate
  - snippet: `input_tensor = torch.randn(1, 1, 6, 6) | indices = torch.argmax(input_tensor, dim=1, keepdim=True) | max_unpool = torch.nn.MaxUnpool2d(2, 2) | pooled = max_unpool(input_tensor, indices)`

### logic_inconsistency_needs_review

- `P3` `VarInconsistentCatch` `torch.Generator` `torch.Generator_2217` source=`Results/torch/valid/torch.Generator_2217.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `generator = torch.Generator() | generator.manual_seed | generator.seed()`
- `P3` `VarInconsistentCatch` `torch.Tensor.add_` `torch.Tensor.add__399` source=`Results/torch/valid/torch.Tensor.add__399.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `device = torch.device('cpu') | data = torch.rand(10, 1, requires_grad=True) | result = torch.Tensor(torch.zeros(10, 1).to(device)) | result = torch.Tensor.add_(result, data) | result = torch.Tensor.add_(result, 5) | result = torch.Tensor.add_(result, 12) | result = torch.Tensor.add_(result, 9)`
- `P3` `VarInconsistentCatch` `torch.Tensor.arcsin_` `torch.Tensor.arcsin__795` source=`Results/torch/valid/torch.Tensor.arcsin__795.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `x = 2 | y = np.pi | result = torch.Tensor.arcsin_((torch.Tensor(x) * y)) | torch.allclose(result, torch.from_numpy(np.array([2, np.pi])).float())`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_179` source=`Results/torch/valid/torch.Tensor.argsort_179.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 3) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, descending=True, dim=(- 2)))[0]`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_200` source=`Results/torch/valid/torch.Tensor.argsort_200.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 3) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, descending=True, dim=0))`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_296` source=`Results/torch/valid/torch.Tensor.argsort_296.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `output_tensor = torch.Tensor.argsort(torch.argsort((torch.randn(3, 4, 5) * 100.0), dim=0)[0][0]) | output_tensor.size()`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_307` source=`Results/torch/valid/torch.Tensor.argsort_307.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0]) | output_tensor.size()`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_371` source=`Results/torch/valid/torch.Tensor.argsort_371.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0], dim=0) | output_tensor.size()`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_373` source=`Results/torch/valid/torch.Tensor.argsort_373.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0], dim=0)`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_375` source=`Results/torch/valid/torch.Tensor.argsort_375.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0], descending=False)`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_376` source=`Results/torch/valid/torch.Tensor.argsort_376.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0], dim=0, descending=False)`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_380` source=`Results/torch/valid/torch.Tensor.argsort_380.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0], dim=0, descending=True)`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_384` source=`Results/torch/valid/torch.Tensor.argsort_384.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0], dim=0)[0]`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_389` source=`Results/torch/valid/torch.Tensor.argsort_389.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0], dim=0, descending=True) | output_tensor.size()`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_394` source=`Results/torch/valid/torch.Tensor.argsort_394.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0], dim=(- 1)) | output_tensor.size()`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_508` source=`Results/torch/valid/torch.Tensor.argsort_508.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(tensor, dim=1, descending=True)[0] | output_tensor = output_tensor.argsort(dim=1, descending=False)[0] | output_tensor = torch.Tensor(output_tensor) | output_tensor.size() | output_tensor = torch.Tensor(output_tensor) | output_tensor = output_tensor.sort()[0] | output_tensor = torch.Tensor(output_tensor)`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_752` source=`Results/torch/valid/torch.Tensor.argsort_752.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(input_tensor, descending=True, dim=1) | output_tensor = torch.Tensor.argsort(output_tensor, descending=True, dim=0) | output_tensor = torch.Tensor.argsort(torch.squeeze(output_tensor), descending=False, dim=0) | output_tensor = output_tensor.sort()[0] | output_tensor = torch.Tensor(output_tensor) | output_tensor.size()`
- `P3` `VarInconsistentCatch` `torch.Tensor.argsort` `torch.Tensor.argsort_797` source=`Results/torch/valid/torch.Tensor.argsort_797.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 4, 5) | output_tensor = torch.Tensor.argsort(input_tensor, dim=1).sort()[1] | output_tensor = output_tensor.sort()[0] | output_tensor = torch.Tensor(output_tensor) | output_tensor.size()`
- `P3` `VarInconsistentCatch` `torch.Tensor.bool` `torch.Tensor.bool_160` source=`Results/torch/valid/torch.Tensor.bool_160.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 5, requires_grad=True) | input_tensor = (input_tensor / torch.sum(input_tensor)) | input_tensor = ((input_tensor - 0.5) * torch.abs(input_tensor)) | input_tensor = (torch.sum(input_tensor, dim=1, keepdim=True) + 0.5) | output = torch.Tensor.bool(torch.rand(3, 3, 5)).bool() | output_ = (input_tensor * output) | output_ = torch.Tensor(output_.size()).zero_()`
- `P3` `VarInconsistentCatch` `torch.Tensor.bool` `torch.Tensor.bool_193` source=`Results/torch/valid/torch.Tensor.bool_193.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(3, 5, requires_grad=True) | input_tensor = (input_tensor / torch.sum(input_tensor)) | input_tensor = ((input_tensor - 0.5) * torch.abs(input_tensor)) | input_tensor = (torch.abs(input_tensor) - 0.5) | input_tensor = torch.abs((torch.mean(input_tensor, dim=1, keepdim=True) + 0.5)) | output = torch.Tensor.bool(torch.rand(3, 3, 5)).bool() | output_ = (input_tensor * output) | output_ = torch.Tensor(output_.size()).zero_()`

### final_output_inconsistency

- `P2` `ComparisonFail` `torch.Tensor.conj_physical_` `torch.Tensor.conj_physical__743` source=`Results/torch/valid/torch.Tensor.conj_physical__743.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `torch.Tensor.conj_physical_(torch.eye(10).to_sparse())`
- `P2` `ComparisonFail` `torch.Tensor.multiply_` `torch.Tensor.multiply__225` source=`Results/torch/valid/torch.Tensor.multiply__225.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `torch.Tensor.multiply_(torch.zeros([3, 2]), torch.tensor([1.0], dtype=torch.float64).to_sparse())`
- `P2` `ComparisonFail` `torch.Tensor.transpose_` `torch.Tensor.transpose__157` source=`Results/torch/valid/torch.Tensor.transpose__157.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `input_tensor = torch.randn(2, 3) | output_tensor = torch.Tensor.transpose_(input_tensor, 0, 1) | if True: | torch.set_default_dtype(torch.float64)`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_1108` source=`Results/torch/valid/torch.dequantize_1108.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | tensor = torch.as_tensor(tensor) | result = torch.dequantize(tensor) | result`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_1262` source=`Results/torch/valid/torch.dequantize_1262.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | dequantized_tensor = torch.dequantize(tensor) | (dequantized_tensor.min(), (dequantized_tensor.max() == 1.0), dequantized_tensor.eq(torch.tensor([0.0, 2.0, 1.0])))`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_129` source=`Results/torch/valid/torch.dequantize_129.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([0.5, 1.5, 2.5]), scale=0.1, zero_point=128, dtype=torch.quint8) | dequantized_tensor = torch.dequantize(tensor)`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_1396` source=`Results/torch/valid/torch.dequantize_1396.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | tensor = tensor.unsqueeze(dim=0) | tensor = torch.as_tensor(tensor) | result = torch.dequantize(tensor) | result`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_1406` source=`Results/torch/valid/torch.dequantize_1406.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | result = [torch.dequantize(tensor)]`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_1416` source=`Results/torch/valid/torch.dequantize_1416.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | result = tensor.dequantize()`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_149` source=`Results/torch/valid/torch.dequantize_149.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | tensor.dequantize()`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_155` source=`Results/torch/valid/torch.dequantize_155.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | dequantized_tensor = tensor.dequantize()`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_1557` source=`Results/torch/valid/torch.dequantize_1557.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=4, zero_point=0, dtype=torch.qint8) | result = torch.dequantize(tensor) | result`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_165` source=`Results/torch/valid/torch.dequantize_165.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | dequantized_tensor = torch.dequantize(tensor) | (dequantized_tensor.min(), (dequantized_tensor.max() == 0.0), dequantized_tensor.eq(torch.tensor([1.0, 2.0, 3.0])))`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_176` source=`Results/torch/valid/torch.dequantize_176.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | dequantized_tensor = torch.dequantize(tensor) | (dequantized_tensor.min(), (dequantized_tensor.max() == 1.0), dequantized_tensor.eq(torch.tensor([(- 1.0), 2.0, 3.0])))`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_2005` source=`Results/torch/valid/torch.dequantize_2005.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | tensor = tensor.unsqueeze(dim=0) | tensor = torch.as_tensor(tensor) | tensor = torch.as_tensor(tensor, dtype=torch.qint8) | result = torch.dequantize(tensor) | result`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_286` source=`Results/torch/valid/torch.dequantize_286.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=2, dtype=torch.qint8) | result = torch.dequantize(tensor)`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_290` source=`Results/torch/valid/torch.dequantize_290.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=2, dtype=torch.qint8) | torch.dequantize(tensor)`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_331` source=`Results/torch/valid/torch.dequantize_331.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | result = torch.dequantize(tensor)`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_337` source=`Results/torch/valid/torch.dequantize_337.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | result = torch.dequantize(tensor) | assert torch.allclose(result, torch.tensor([1.0, 2.0, 3.0]))`
- `P2` `ComparisonFail` `torch.dequantize` `torch.dequantize_340` source=`Results/torch/valid/torch.dequantize_340.py`
  - reason: CPU/GPU inconsistency without an obvious low-value pattern
  - snippet: `tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8) | result = torch.dequantize(tensor) | result = result.squeeze()`

### strong_backend_failure

- `P1` `FrameworkCrashCatch` `torch.distributed.algorithms.JoinHook` `torch.distributed.algorithms.JoinHook_6120` source=`Results/torch/exception/torch.distributed.algorithms.JoinHook_6120.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - snippet: `hook = torch.distributed.algorithms.JoinHook() | hook = hook.__class__() | hook.on_worker_init_called = True | global distributed | distributed = DistributedBuilder(DDPConfig(worker_devices=[], world_size=1), [hook.build()]) | hook.on_worker_init_called = False`
- `P1` `FrameworkCrashCatch` `torch.distributed.gather_object` `torch.distributed.gather_object_496` source=`Results/torch/exception/torch.distributed.gather_object_496.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - snippet: `global object_gather_list | obj = {'key': 'value'} | object_gather_list = [None] | torch.distributed.gather_object(obj, object_gather_list) | for obj in object_gather_list: | print(obj)`
- `P1` `FrameworkCrashCatch` `torch.distributions.exp_family.ExponentialFamily` `torch.distributions.exp_family.ExponentialFamily_69` source=`Results/torch/exception/torch.distributions.exp_family.ExponentialFamily_69.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - snippet: `input_data = {} | output = torch.distributions.exp_family.ExponentialFamily(input_data={**input_data, **kwargs})`
- `P1` `FrameworkCrashCatch` `torch.nn.ModuleDict` `torch.nn.ModuleDict_282` source=`Results/torch/exception/torch.nn.ModuleDict_282.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - snippet: `new_modules = {**old_modules, **new_modules} | new_module_dict = torch.nn.ModuleDict(new_modules)`
- `P1` `FrameworkCrashCatch` `torch.nn.ModuleDict` `torch.nn.ModuleDict_505` source=`Results/torch/exception/torch.nn.ModuleDict_505.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - snippet: `modules = {'conv1': torch.nn.Conv2d(1, 64, kernel_size=3), 'fc1': torch.nn.Linear(9216, 512)} | model_dict = torch.nn.ModuleDict(modules) | state_dict = {k: v for (k, v) in model_dict.state_dict().items()} | new_state_dict = {**state_dict, **new_modules}`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1117` source=`Results/torch/valid/torch.nn.RNNBase_1117.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1155` source=`Results/torch/valid/torch.nn.RNNBase_1155.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1156` source=`Results/torch/valid/torch.nn.RNNBase_1156.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1157` source=`Results/torch/exception/torch.nn.RNNBase_1157.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1158` source=`Results/torch/valid/torch.nn.RNNBase_1158.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1159` source=`Results/torch/valid/torch.nn.RNNBase_1159.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1160` source=`Results/torch/exception/torch.nn.RNNBase_1160.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1161` source=`Results/torch/exception/torch.nn.RNNBase_1161.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1162` source=`Results/torch/exception/torch.nn.RNNBase_1162.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1163` source=`Results/torch/exception/torch.nn.RNNBase_1163.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1164` source=`Results/torch/valid/torch.nn.RNNBase_1164.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1165` source=`Results/torch/exception/torch.nn.RNNBase_1165.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1166` source=`Results/torch/exception/torch.nn.RNNBase_1166.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1167` source=`Results/torch/exception/torch.nn.RNNBase_1167.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`
- `P1` `GpuCrashCatch` `torch.nn.RNNBase` `torch.nn.RNNBase_1168` source=`Results/torch/exception/torch.nn.RNNBase_1168.py`
  - reason: native crash/internal assert style signal; verify with an independent minimal repro
  - evidence: `INTERNAL ASSERT FAILED, please report a bug`
  - snippet: `mode = 'RNN_TANH' | input_size = 10 | hidden_size = 20 | batch_first = True | device = torch.device('cpu') | rnn_base = torch.nn.RNNBase(mode, input_size, hidden_size, batch_first=batch_first, device=device) | with torch.no_grad(): | lstm_base = torch.nn.LSTM(input_size, hidden_size, batch_first=batch_first, num_layers=1, device=device)`

### gpu_exec_or_cuda_assert_mismatch

- `P2` `GpuExecFail` `torch.LongStorage` `torch.LongStorage_247` source=`Results/torch/valid/torch.LongStorage_247.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `data = torch.LongTensor([1, 2, 3]) | result = torch.LongStorage(data.size()[0]) | data[0] = 100 | result[1] = 200`
- `P2` `GpuExecFail` `torch.Tensor.bernoulli_` `torch.Tensor.bernoulli__1470` source=`Results/torch/valid/torch.Tensor.bernoulli__1470.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `y = torch.Tensor.bernoulli_(torch.Tensor.bernoulli_(torch.randn(1)))`
- `P2` `GpuExecFail` `torch.Tensor.nanquantile` `torch.Tensor.nanquantile_208` source=`Results/torch/valid/torch.Tensor.nanquantile_208.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `_input_tensor = torch.tensor([1.0, float('nan'), 3.0, 4.0]) | q = torch.Tensor([0.0]) | result = torch.Tensor.nanquantile(_input_tensor, q)`
- `P2` `GpuExecFail` `torch.Tensor.new_full` `torch.Tensor.new_full_537` source=`Results/torch/valid/torch.Tensor.new_full_537.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `_input_tensor = torch.randn(4, 4) | _output_tensor = torch.Tensor.new_full(_input_tensor, size=(4, 4), fill_value=2.0, dtype=torch.float64) | _loss = torch.nn.MSELoss(reduction='mean') | _loss.forward(_input_tensor, _output_tensor)`
- `P2` `GpuExecFail` `torch.broadcast_shapes` `torch.broadcast_shapes_935` source=`Results/torch/valid/torch.broadcast_shapes_935.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `a = (torch.ones((1, 2, 3, 4)).type(torch.float32) / 3.0) | b = a | result = torch.broadcast_shapes(a.shape, b.shape, a.shape)`
- `P2` `GpuExecFail` `torch.index_select` `torch.index_select_1111` source=`Results/torch/valid/torch.index_select_1111.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `input_tensor = torch.randn(3, 4, 3, 2) | input_tensor = input_tensor.to(torch.device('cpu')) | dim = 1 | index = torch.tensor(torch.arange(input_tensor.size(0), device=input_tensor.device)) | index = torch.cat(torch.meshgrid(index.view((- 1)), index.view((- 1))), dim=dim) | index = index.flatten() | result = torch.index_select(input_tensor, dim, index) | result = torch.tensor(result.cpu())`
- `P2` `GpuExecFail` `torch.lu` `torch.lu_752` source=`Results/torch/valid/torch.lu_752.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `A = torch.tensor([[4.0, 3.0], [6.0, 3.0]]) | (lu, pivots) = torch.lu(A, pivot=True, get_infos=False) | (lu, pivots)`
- `P2` `GpuExecFail` `torch.nn.functional.binary_cross_entropy` `torch.nn.functional.binary_cross_entropy_1506` source=`Results/torch/valid/torch.nn.functional.binary_cross_entropy_1506.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `target = torch.ones(10, 100) | output = torch.sigmoid(torch.randn(10, 100)) | output = torch.sigmoid(output) | loss = torch.sum((torch.nn.functional.binary_cross_entropy(output, target, reduction='mean') * ((output > 0.5) ** 2))) | loss.mean()`
- `P2` `GpuExecFail` `torch.nn.functional.fractional_max_pool3d` `torch.nn.functional.fractional_max_pool3d_584` source=`Results/torch/valid/torch.nn.functional.fractional_max_pool3d_584.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, AcceleratorError CUDA error`
  - snippet: `x = torch.randn(100, 3, 128, 128) | x = torch.relu(x) | x = torch.clamp(x, min=0.0, max=1.0) | x = torch.reshape(x, ((- 1), 4, 4, 4)).type(torch.FloatTensor) | x = x.type(torch.FloatTensor) | output_size = (2, 2, 2) | fractional_stride = (1, 1, 1) | random_samples = torch.rand(100, 3, 128, 128)`
- `P2` `GpuExecFail` `torch.nn.functional.fractional_max_pool3d` `torch.nn.functional.fractional_max_pool3d_590` source=`Results/torch/valid/torch.nn.functional.fractional_max_pool3d_590.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, AcceleratorError CUDA error`
  - snippet: `x = torch.randn(100, 3, 128, 128) | x = torch.relu(torch.relu(x)) | x = torch.relu(x) | x = torch.clamp(x, min=0.0, max=1.0) | x = torch.reshape(x, ((- 1), 2, 2)) | x = x.view((- 1), 4, 4, 4) | x = x.type(torch.FloatTensor) | x = x.type(torch.FloatTensor)`
- `P2` `GpuExecFail` `torch.nn.functional.fractional_max_pool3d` `torch.nn.functional.fractional_max_pool3d_614` source=`Results/torch/valid/torch.nn.functional.fractional_max_pool3d_614.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, AcceleratorError CUDA error`
  - snippet: `x = torch.randn(100, 3, 256, 256) | x = torch.relu(x) | x = torch.clamp(x, min=0.0, max=1.0) | x = torch.reshape(x, ((- 1), 4, 4, 4)).type(torch.FloatTensor) | x = x.type(torch.FloatTensor) | output_size = (2, 2, 2) | fractional_stride = (1, 1, 1) | random_samples = torch.rand(100, 3, 128, 128)`
- `P2` `GpuExecFail` `torch.nn.functional.gumbel_softmax` `torch.nn.functional.gumbel_softmax_326` source=`Results/torch/valid/torch.nn.functional.gumbel_softmax_326.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `logits = torch.tensor([[0.5, (- 0.2), 0.8], [(- 0.1), 0.7, 0.4]]) | tau = 1.0 | logits = (logits + (torch.randn(*logits.shape) * tau)) | output = torch.nn.functional.gumbel_softmax(logits, tau=1.0) | output = (output / torch.sum(output, dim=1, keepdim=True)) | predict = torch.nn.functional.log_softmax(output, dim=(- 1)) | predict = (predict / torch.sum(predict, dim=1, keepdim=True)) | predict = predict.detach().numpy()`
- `P2` `GpuExecFail` `torch.nn.utils.rnn.pack_padded_sequence` `torch.nn.utils.rnn.pack_padded_sequence_1517` source=`Results/torch/valid/torch.nn.utils.rnn.pack_padded_sequence_1517.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `input_data = torch.autograd.Variable(torch.rand(4, 5, 6, 7)) | lengths = [5, 4, 3, 2] | packed_seq = torch.nn.utils.rnn.pack_padded_sequence(input_data, lengths, batch_first=True) | (sequence, _) = torch.nn.utils.rnn.pad_packed_sequence(packed_seq, batch_first=True) | output_data = sequence.index_select(dim=1, index=torch.LongTensor([2, 3])).type_as(sequence) | (output_data.size() == torch.Size([5, 4, 6, 7])) | (torch.autograd.Variable(output_data) == output_data)`
- `P2` `GpuExecFail` `torch.nn.utils.rnn.pack_sequence` `torch.nn.utils.rnn.pack_sequence_1030` source=`Results/torch/valid/torch.nn.utils.rnn.pack_sequence_1030.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `sequences = [torch.tensor([1, 2]), torch.tensor([3, 4, 5])] | sorted_sequences = sorted(sequences, key=len, reverse=True) | packed_sequences = torch.nn.utils.rnn.pack_sequence(sorted_sequences) | unpacked_sequences = packed_sequences[0] | packed = torch.nn.utils.rnn.pad_packed_sequence(packed_sequences, batch_first=True) | inputs = torch.zeros(6, 2) | unpacked_sequences = packed[0] | input_seq = packed_sequences[0][0]`
- `P2` `GpuExecFail` `torch.take_along_dim` `torch.take_along_dim_1255` source=`Results/torch/valid/torch.take_along_dim_1255.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `input_tensor = torch.randn(5, 3, 10) | indices = torch.arange(5, dtype=torch.long, device=torch.device('cpu')) | result = torch.take_along_dim(input_tensor, indices, out=torch.ones(3, 1)) | result.detach_() | result = result.detach()`
- `P2` `GpuExecFail` `torch.tril_indices` `torch.tril_indices_148` source=`Results/torch/valid/torch.tril_indices_148.py`
  - reason: CPU/GPU behavior may differ; run CPU and CUDA in independent processes
  - evidence: `device-side assert, cudaErrorAssert, AcceleratorError CUDA error`
  - snippet: `row = 5 | col = 4 | (row, col) = torch.LongTensor([row, col]) | indices = torch.tril_indices(col, row)`

## Suggested Server Review Command

```bash
cd /workspace/TitanFuzz
python TensorGuard-Repros/scripts/generate_trace_logic_review.py \
  --results-dir Results/torch \
  --repo-dir TensorGuard-Repros
```

Then start manual reproduction from `logic_focus_candidates.tsv`, P1 first, then P2.
