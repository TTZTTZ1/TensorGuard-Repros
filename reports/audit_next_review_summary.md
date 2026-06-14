# 下一轮 P1/P2 审核结论

更新日期：2026-06-14

## 结论

本轮基于 `logs/audit_next/queues/` 重新筛选出的高优先级候选进行了两批复核：

- P1 strong crash/internal assert 第一批：`1-10`
- P1 diverse batch：`430-467`
- P2 direct exception mismatch：`1-10`

结论：本轮没有新增可以直接收录的 PyTorch bug。后续不建议继续盲跑 P1/P2 大队列，应转向整理和最小化已有高价值候选。

## P1 第一批：1-10

结果目录：

```text
logs/audit_next/runs/p1_strong_crash_or_internal_assert/
```

审核结论：

- `torch.sparse.mm_1075`
- `torch.sparse.mm_1087`
- `torch.sparse.mm_1580`
- `torch.sparse.mm_235`
- `torch.sparse.mm_400`

这些候选没有真正复现 PyTorch crash，运行时首先遇到源码三引号未闭合：

```text
unterminated triple-quoted string literal
```

暂不收录。

- `torch.sparse_csr_tensor_1011`
- `torch.sparse_csr_tensor_517`
- `torch.sparse_csr_tensor_858`
- `torch.sparse_csr_tensor_901`

这些候选在 `torch2cuda` 对比阶段遇到：

```text
ComparisonFail unsupported tensor layout: SparseCsr
```

这更像工具比较器不支持 SparseCsr，而不是新 PyTorch bug。Sparse crash 家族已经有之前的最小复现作为代表。

- `torch.nn.RNNBase_1109`

源码语法不完整：

```text
expected an indented block after 'for' statement
```

暂不收录。

## P1 diverse：430-467

结果目录：

```text
logs/audit_next/runs/p1_strong_crash_or_internal_assert/
```

`interesting_hits.txt` 为空。逐项查看后，主要结果为：

- `No problem found`
- CPU/GPU 同样普通异常
- Python 语法错误
- 生成代码变量未定义
- 普通 `TypeError` / `AttributeError` / `ValueError`

没有复现：

- `INTERNAL ASSERT FAILED`
- `please report a bug`
- `free()`
- `Segmentation fault`
- `Floating point exception`
- `Check failed`

因此本批不收录。

## P2 direct exception mismatch：1-10

结果目录：

```text
logs/audit_next/runs/p2_direct_exception_mismatch/
```

逐项结论：

| 序号 | 候选 | 结论 |
|---:|---|---|
| 1 | `torch.LongStorage_300` | 不收录。代码 `.to(data.size()[0])` 被解释为迁移到 CUDA device 3，当前环境不存在该 GPU，CPU/GPU 都是 `invalid device ordinal`。 |
| 2 | `torch.Tensor.is_set_to_1457` | 不收录。`No problem found`。 |
| 3 | `torch.Tensor.polygamma__1265` | 不收录。`No problem found`。 |
| 4 | `torch.Tensor.unfold_1272` | 不收录。CPU/GPU 都是相同 shape mismatch RuntimeError。 |
| 5 | `torch.concat_221` | 不收录。生成代码中 `device` 未定义。 |
| 6 | `torch.gather_2057` | 不收录。`No problem found`。 |
| 7 | `torch.nn.utils.skip_init_4193` | 不收录。生成代码中 `kwargs` 未定义。 |
| 8 | `torch.set_num_interop_threads_1033` | 不收录。源码三引号未闭合。 |
| 9 | `torch.utils.data.WeightedRandomSampler_1176` | 不收录。`No problem found`。 |
| 10 | `torch.utils.data.WeightedRandomSampler_964` | 不收录。`No problem found`。 |

## P2 index exception focus：1-10

结果目录：

```text
logs/audit_next/runs/p2_index_exception_focus/
```

本批按 API 家族从 `trace_cpu_gpu_exception_mismatch` 中抽取索引/越界类候选，避免被大量重复 `ByteStorage` 候选淹没。

逐项结论：

| 序号 | 候选 | 结论 |
|---:|---|---|
| 1 | `torch.Tensor.gather_109` | 待独立复测。`torch2cuda` 同进程 duel 中 CPU/GPU 都显示 `AcceleratorError CUDA error: device-side assert triggered`，疑似 CUDA 上下文污染。源码注释指向 `index 3 is out of bounds for dimension 1 with size 3`，如果独立 CPU/GPU 进程分别表现为 CPU `RuntimeError`、CUDA device-side assert，可作为 C3 的新 API 证据。 |
| 2 | `torch.Tensor.index_copy_1083` | 不收录。CPU/GPU 都是相同 `IndexError`: source/destination 维度不匹配。 |
| 3 | `torch.Tensor.index_fill_100` | 不收录。生成代码变量 `input_tensor_shape` 未定义。 |
| 4 | `torch.Tensor.index_select_1011` | 不收录。`No problem found`。 |
| 5 | `torch.Tensor.scatter__1018` | 不收录。生成代码变量 `output_tensor` 未定义。 |
| 6 | `torch.Tensor.take_1002` | 待独立复测。`torch2cuda` 同进程 duel 中 CPU/GPU 都显示 CUDA device-side assert，疑似 CUDA 上下文污染。源码片段为长度 2 张量配 `torch.arange(3)`，应检查独立进程下 CPU 是否为 out-of-range `RuntimeError`、CUDA 是否为 device-side assert。 |
| 7 | `torch.gather_1034` | 不收录。生成代码 `torch.arange(5)(5, 4)` 把 Tensor 当函数调用，CPU/GPU 同样 `TypeError`。 |
| 8 | `torch.nn.functional.cross_entropy_1080` | 不收录。生成代码使用错误参数名 `weights`，CPU/GPU 同样 `TypeError`。 |
| 9 | `torch.nn.functional.embedding_109` | 不收录。生成代码变量 `input_data` 未定义。 |
| 10 | `torch.nn.functional.nll_loss_1012` | 不收录。`No problem found`。 |

本批暂不新增 confirmed candidate。
下一步只需对 `gather` 和 `take` 做独立 CPU/GPU 进程最小复现，不建议继续直接顺序跑 5 万多个 trace P2 候选。

## 下一步建议

停止继续盲跑：

- P1 中 `torch.nn.RNNBase_*` 大段候选
- P2 中 `trace_cpu_gpu_exception_mismatch` 的 5 万多个候选

这些候选大概率来自 trace 附近污染或生成代码问题，继续跑性价比很低。

下一步应该整理已有候选：

1. 保留高价值候选：`torch.is_nonzero` internal assert。
2. 保留次高价值候选：sparse invalid invariant 触发 native crash，但必须明确 sparse invariant caveat。
3. 保留中等价值候选：CPU 正常 `RuntimeError`，CUDA `device-side assert` 的异常语义不一致类。
4. 下调或移除 alias/out 相关候选，避免被认为不是 PyTorch bug。
