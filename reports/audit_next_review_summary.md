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
