# Next PyTorch Audit Queues

This queue is generated from TitanFuzz result files and trace evidence.

Ranking policy:
- P1: internal assert, native crash, abort, `free()`, FPE, segfault, `Check failed`.
- P2: CPU/GPU exception mismatch, especially CUDA device-side assert.
- P3: clean CPU/GPU logic inconsistency after filtering obvious alias/numpy/resize/noisy patterns.

Known senior-review adjustment:
- Previously collected `out=input`, in-place alias, transpose-view alias, and numpy-view cases are not prioritized as PyTorch bugs.
- Sparse invariant crashes are kept as evidence family, but new sparse candidates need the invariant caveat checked.

Total candidates before already-reviewed filtering: 64638
Total unreviewed candidates: 58380

Unreviewed by priority: {'P1': 490, 'P2': 57890}
Unreviewed by bucket: {'cpu_gpu_exception_mismatch': 10, 'strong_crash_or_internal_assert': 46, 'trace_cpu_gpu_exception_mismatch': 57880, 'trace_strong_crash_or_internal_assert': 444}

## Top P1

- torch.sparse.mm_1075 | Results/torch/crash/torch.sparse.mm_1075.py | free\(\):, invalid pointer, returncode=-6
- torch.sparse.mm_1087 | Results/torch/crash/torch.sparse.mm_1087.py | free\(\):, invalid pointer, returncode=-6
- torch.sparse.mm_1580 | Results/torch/crash/torch.sparse.mm_1580.py | free\(\):, invalid pointer, returncode=-6
- torch.sparse.mm_235 | Results/torch/crash/torch.sparse.mm_235.py | free\(\):, invalid pointer, returncode=-6
- torch.sparse.mm_400 | Results/torch/crash/torch.sparse.mm_400.py | free\(\):, invalid pointer, returncode=-6
- torch.sparse_csr_tensor_1011 | Results/torch/crash/torch.sparse_csr_tensor_1011.py | free\(\):, invalid next size, returncode=-6
- torch.sparse_csr_tensor_517 | Results/torch/crash/torch.sparse_csr_tensor_517.py | free\(\):, invalid next size, returncode=-6
- torch.sparse_csr_tensor_858 | Results/torch/crash/torch.sparse_csr_tensor_858.py | free\(\):, invalid next size, returncode=-6
- torch.sparse_csr_tensor_901 | Results/torch/crash/torch.sparse_csr_tensor_901.py | free\(\):, invalid next size, returncode=-6
- torch.nn.RNNBase_1109 | Results/torch/exception/torch.nn.RNNBase_1109.py | INTERNAL ASSERT FAILED
- torch.nn.RNNBase_111 | Results/torch/exception/torch.nn.RNNBase_111.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1110 | Results/torch/exception/torch.nn.RNNBase_1110.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1111 | Results/torch/exception/torch.nn.RNNBase_1111.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1112 | Results/torch/exception/torch.nn.RNNBase_1112.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1113 | Results/torch/valid/torch.nn.RNNBase_1113.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1114 | Results/torch/valid/torch.nn.RNNBase_1114.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1115 | Results/torch/valid/torch.nn.RNNBase_1115.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1116 | Results/torch/exception/torch.nn.RNNBase_1116.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1117 | Results/torch/valid/torch.nn.RNNBase_1117.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1119 | Results/torch/exception/torch.nn.RNNBase_1119.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_112 | Results/torch/exception/torch.nn.RNNBase_112.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1148 | Results/torch/exception/torch.nn.RNNBase_1148.py | INTERNAL ASSERT FAILED
- torch.nn.RNNBase_115 | Results/torch/exception/torch.nn.RNNBase_115.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1150 | Results/torch/exception/torch.nn.RNNBase_1150.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1151 | Results/torch/exception/torch.nn.RNNBase_1151.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1153 | Results/torch/exception/torch.nn.RNNBase_1153.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1154 | Results/torch/exception/torch.nn.RNNBase_1154.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1155 | Results/torch/valid/torch.nn.RNNBase_1155.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1156 | Results/torch/valid/torch.nn.RNNBase_1156.py | INTERNAL ASSERT FAILED, please report a bug
- torch.nn.RNNBase_1157 | Results/torch/exception/torch.nn.RNNBase_1157.py | INTERNAL ASSERT FAILED, please report a bug

## Top P2

- torch.ByteStorage_950 | Results/torch/exception/torch.ByteStorage_950.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_951 | Results/torch/valid/torch.ByteStorage_951.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_952 | Results/torch/exception/torch.ByteStorage_952.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_953 | Results/torch/valid/torch.ByteStorage_953.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_954 | Results/torch/exception/torch.ByteStorage_954.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_955 | Results/torch/exception/torch.ByteStorage_955.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_956 | Results/torch/exception/torch.ByteStorage_956.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_957 | Results/torch/valid/torch.ByteStorage_957.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_958 | Results/torch/valid/torch.ByteStorage_958.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_959 | Results/torch/exception/torch.ByteStorage_959.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_96 | Results/torch/exception/torch.ByteStorage_96.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_960 | Results/torch/valid/torch.ByteStorage_960.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_961 | Results/torch/valid/torch.ByteStorage_961.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_962 | Results/torch/exception/torch.ByteStorage_962.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_964 | Results/torch/valid/torch.ByteStorage_964.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_965 | Results/torch/valid/torch.ByteStorage_965.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_966 | Results/torch/exception/torch.ByteStorage_966.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_967 | Results/torch/exception/torch.ByteStorage_967.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_968 | Results/torch/valid/torch.ByteStorage_968.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_969 | Results/torch/exception/torch.ByteStorage_969.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_97 | Results/torch/exception/torch.ByteStorage_97.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_970 | Results/torch/valid/torch.ByteStorage_970.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_971 | Results/torch/valid/torch.ByteStorage_971.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_972 | Results/torch/valid/torch.ByteStorage_972.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_973 | Results/torch/valid/torch.ByteStorage_973.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_974 | Results/torch/valid/torch.ByteStorage_974.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_976 | Results/torch/valid/torch.ByteStorage_976.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_977 | Results/torch/valid/torch.ByteStorage_977.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_978 | Results/torch/valid/torch.ByteStorage_978.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error
- torch.ByteStorage_98 | Results/torch/exception/torch.ByteStorage_98.py | device-side assert, cudaErrorAssert, AcceleratorError CUDA error

## Top P3

