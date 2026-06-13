# API Focus Review Report

本报告按 API 聚合，只列出需要人工重点考虑的错误源码；生成代码错误和普通参数错误不进入本报告主体，但会在 TSV 中完整记录。

## Overall

- Scanned source files: 828983
- Focus candidates: 35
- APIs with focus candidates: 4

Focus categories:
- `strong_backend_failure`: 2
- `strong_backend_failure_sparse_caveat`: 33

All categories, including excluded ones:
- `common_user_or_argument_error`: 182128
- `generated_code_error`: 201181
- `low_signal_unclassified_exception`: 164710
- `no_embedded_error_signal`: 278306
- `strong_backend_failure`: 2
- `strong_backend_failure_sparse_caveat`: 33
- `tool_or_environment_limit`: 2623

## APIs

### torch.is_nonzero

Focus candidates: 1

- `torch.is_nonzero_2006` `notarget` `strong_backend_failure`
  - path: `Results/torch/notarget/torch.is_nonzero_2006.py`
  - signal: INTERNAL ASSERT FAILED, please report a bug
  - message: scalar.isIntegral( false) INTERNAL ASSERT FAILED at "/pytorch/torch/csrc/utils/pybind.cpp":27, please report a bug to PyTorch.
  - trigger: 2: result = torch.eye(torch.any(torch.not_equal(torch.eye(2).bool(), 1.0)))
  - snippet: `result = torch.eye(torch.any(torch.not_equal(torch.eye(2).bool(), 1.0))) | assert result`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed

### torch.package.PackageExporter

Focus candidates: 1

- `torch.package.PackageExporter_635` `crash` `strong_backend_failure`
  - path: `Results/torch/crash/torch.package.PackageExporter_635.py`
  - signal: returncode=-6
  - message: returncode=-6
  - trigger: 4: exporter = torch.package.PackageExporter(f)
  - snippet: `f = torch.arange(10000, dtype=torch.float) | exporter = torch.package.PackageExporter(f)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed

### torch.sparse.mm

Focus candidates: 8

- `torch.sparse.mm_1075` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse.mm_1075.py`
  - signal: free\(\):, invalid pointer, returncode=-6
  - message: returncode=-6
  - trigger: 5: _result = torch.sparse.mm(mat1, mat2)
  - snippet: `mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3)) | mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 2], [2, 3]]), values=torch.tensor([3.0, 4.0]), size=(3, 2)) | _result = torch.sparse.mm(mat1, mat2)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse.mm_1087` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse.mm_1087.py`
  - signal: free\(\):, invalid pointer, returncode=-6
  - message: returncode=-6
  - trigger: 5: _result = torch.sparse.mm(mat1, mat2)
  - snippet: `mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3)) | mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 2], [0, 3]]), values=torch.tensor([1.0, 2.0]), size=(3, 2)) | _result = torch.sparse.mm(mat1, mat2)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse.mm_142` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse.mm_142.py`
  - signal: free\(\):, invalid pointer, returncode=-6
  - message: returncode=-6
  - trigger: 5: _result = torch.sparse.mm(mat1, mat2)
  - snippet: `mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3)) | mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 2], [2, 3]]), values=torch.tensor([1.0, 3.0]), size=(3, 2)) | _result = torch.sparse.mm(mat1, mat2)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse.mm_1580` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse.mm_1580.py`
  - signal: free\(\):, invalid pointer, returncode=-6
  - message: returncode=-6
  - trigger: 5: _result = torch.sparse.mm(mat1, mat2)
  - snippet: `mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3)) | mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[1, 2], [3, 0]]), values=torch.tensor([1.0, 2.0]), size=(3, 2)) | _result = torch.sparse.mm(mat1, mat2)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse.mm_235` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse.mm_235.py`
  - signal: free\(\):, invalid pointer, returncode=-6
  - message: returncode=-6
  - trigger: 5: _result = torch.sparse.mm(mat1, mat2)
  - snippet: `mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3)) | mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [2, 3]]), values=torch.tensor([(- 1.0), 1.0]), size=(3, 2)) | _result = torch.sparse.mm(mat1, mat2)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse.mm_280` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse.mm_280.py`
  - signal: returncode=-6
  - message: returncode=-6
  - trigger: 5: _result = torch.sparse.mm(mat1, mat2)
  - snippet: `mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3)) | mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [2, 3]]), values=torch.tensor([3.0, 4.0]), size=(3, 3)) | _result = torch.sparse.mm(mat1, mat2)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse.mm_400` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse.mm_400.py`
  - signal: free\(\):, invalid pointer, returncode=-6
  - message: returncode=-6
  - trigger: 5: _result = torch.sparse.mm(mat1, mat2)
  - snippet: `mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3)) | mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [2, 3]]), values=torch.tensor([1.0, 3.0]), size=(3, 3)) | _result = torch.sparse.mm(mat1, mat2) | torch._assert_no_grad(_result)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse.mm_45` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse.mm_45.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 5: _result = torch.sparse.mm(mat2, mat1)
  - snippet: `mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3)) | mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [2, 0]]), values=torch.tensor([3.0, 4.0]), size=(3, 2)) | _result = torch.sparse.mm(mat2, mat1)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认

### torch.sparse_csr_tensor

Focus candidates: 25

- `torch.sparse_csr_tensor_1011` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_1011.py`
  - signal: free\(\):, invalid next size, returncode=-6
  - message: returncode=-6
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.randn(2, 3) | torch.mm(sparse_tensor, torch.eye(2)) | torch.mm(sparse_tensor, m) | m = torch.zeros((3, 2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_1346` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_1346.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.diag(torch.tensor([1, 2, 3, 4])) | torch.matmul(sparse_tensor, sparse_tensor.t()) | torch.matmul(sparse_tensor, sparse_tensor.t().conj()) | torch.eye(3)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_1364` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_1364.py`
  - signal: returncode=-6
  - message: returncode=-6
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.zeros((2, 2), device=torch.device('cpu'), requires_grad=True) | m = m.mm(sparse_tensor) | m = m.mul(sparse_tensor) | torch.mm(sparse_tensor, torch.eye(2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_1379` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_1379.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.randn(2, 3) | torch.set_default_tensor_type(torch.FloatTensor) | torch.mm(sparse_tensor, torch.eye(2)) | torch.mm(sparse_tensor, sparse_tensor.t())`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_1400` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_1400.py`
  - signal: returncode=-6
  - message: returncode=-6
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.randn(2, 3) | torch.set_default_tensor_type(torch.FloatTensor) | torch.mm(sparse_tensor, torch.eye(2)) | torch.mm(torch.eye(2), sparse_tensor)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_1412` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_1412.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.randn(2, 3) | torch.set_default_tensor_type(torch.FloatTensor) | torch.mm(sparse_tensor, torch.eye(2)) | torch.mm(sparse_tensor, sparse_tensor.t())`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_1427` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_1427.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.randn(2, 3) | torch.set_printoptions(precision=3) | torch.set_printoptions(threshold=10) | torch.mm(sparse_tensor, torch.eye(2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_1454` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_1454.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.randn(2, 3) | torch.set_printoptions(precision=3) | torch.set_printoptions(threshold=10) | torch.mm(sparse_tensor, torch.eye(2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_1577` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_1577.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.randn(2, 3) | torch.mm(sparse_tensor, torch.eye(2)) | torch.mm(sparse_tensor, m) | torch.mm(sparse_tensor, sparse_tensor.t())`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_513` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_513.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, sparse_tensor.t()) | torch.sparse.add(sparse_tensor, sparse_tensor, sparse_tensor) | sparse_tensor.sum(dim=0).sum(dim=1, keepdim=True)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_515` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_515.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, sparse_tensor.t()) | result = torch.mv(sparse_tensor, sparse_tensor)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_516` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_516.py`
  - signal: free\(\):, invalid next size, returncode=-6
  - message: returncode=-6
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, sparse_tensor.t())`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_517` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_517.py`
  - signal: free\(\):, invalid next size, returncode=-6
  - message: returncode=-6
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, sparse_tensor.t()) | torch.mm(sparse_tensor.t(), sparse_tensor)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_528` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_528.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, sparse_tensor.transpose((- 1), (- 2))) | torch.mm(sparse_tensor, sparse_tensor.transpose((- 1), (- 2)))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_533` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_533.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, sparse_tensor.t()) | result`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_562` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_562.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(2) | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, torch.eye(2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_565` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_565.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(3, dtype=torch.long).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, torch.eye(2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_587` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_587.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | torch.mm(sparse_tensor, sparse_tensor.t())`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_858` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_858.py`
  - signal: free\(\):, invalid next size, returncode=-6
  - message: returncode=-6
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(5).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | result = torch.mm(sparse_tensor, sparse_tensor.t()) | torch.mm(sparse_tensor, torch.eye(2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_871` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_871.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(5).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | result = torch.mm(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, sparse_tensor.t()) | torch.mm(sparse_tensor.t(), sparse_tensor) | torch.eye(2)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_897` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_897.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | torch.matmul(sparse_tensor, sparse_tensor) | torch.mm(sparse_tensor, sparse_tensor.transpose(0, 1))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_901` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_901.py`
  - signal: free\(\):, invalid next size, returncode=-6
  - message: returncode=-6
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | torch.matmul(sparse_tensor, sparse_tensor) | torch.matmul(sparse_tensor, sparse_tensor.t()) | torch.mm(sparse_tensor, torch.eye(2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_912` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_912.py`
  - signal: returncode=-6
  - message: returncode=-6
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | torch.matmul(sparse_tensor, sparse_tensor) | torch.matmul(sparse_tensor, sparse_tensor.t()) | torch.matmul(sparse_tensor, torch.eye(2)) | torch.matmul(sparse_tensor, (torch.eye(2) * 2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_918` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_918.py`
  - signal: returncode=-11
  - message: returncode=-11
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | torch.matmul(sparse_tensor, sparse_tensor) | torch.allclose(torch.eye(2), torch.mm(sparse_tensor, sparse_tensor.t())) | torch.mm(sparse_tensor, torch.eye(2))`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认
- `torch.sparse_csr_tensor_988` `crash` `strong_backend_failure_sparse_caveat`
  - path: `Results/torch/crash/torch.sparse_csr_tensor_988.py`
  - signal: returncode=-6
  - message: returncode=-6
  - trigger: 6: sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
  - snippet: `row_indices = torch.arange(4, dtype=torch.int64).long() | col_indices = torch.tensor([0, 2, 1, 3]) | values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu')) | sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2])) | m = torch.randn(2, 3) | torch.mm(sparse_tensor, torch.eye(2)) | torch.mm(sparse_tensor, m) | torch.matmul(sparse_tensor, m)`
  - action: 匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed；但 sparse invariant 需要单独确认

