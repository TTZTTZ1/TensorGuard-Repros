# 下一轮 PyTorch Bug 审核方案

这轮不再优先审核 `out=input`、原地 alias、转置 view alias、`.numpy()` 共享内存、`.resize_()` 读未初始化内存这类候选。学长已经指出这些更像生成程序本身触发的未定义/不稳定行为，不适合作为主要 PyTorch bug 证据。

现在按论文附录中已发现 bug 的风格重新筛选：优先找内部断言、进程崩溃、内存破坏、FPE、C++ `Check failed`、CPU/GPU 异常语义不一致。

## 优先级

P1：强崩溃 / 内部断言

- `INTERNAL ASSERT FAILED`
- `please report a bug`
- `Segmentation fault`
- `Floating point exception`
- `double free`
- `free(): invalid pointer`
- `free(): invalid next size`
- `corruption`
- `Check failed`
- `returncode=134/136/139`

P2：CPU/GPU 异常语义不一致

- CPU 是正常 Python `RuntimeError`
- GPU 触发 `CUDA device-side assert` / `cudaErrorAssert` / `AcceleratorError`

P3：干净的 CPU/GPU 输出不一致

- 只作为低优先级候选
- 必须排除 alias、`out=`、原地 `_`、`.resize_()`、`.numpy()`、未初始化内存、TF32 数值误差、`log/sqrt/pow` 数值边界放大

## 服务器运行方法

在服务器 TitanFuzz 根目录执行：

```bash
cd /workspace/TitanFuzz
git -C TensorGuard-Repros pull --ff-only
```

生成下一轮队列，结果会直接写进共享仓库目录：

```bash
python TensorGuard-Repros/scripts/generate_next_audit_queue.py \
  --results-dir Results/torch \
  --repo-dir TensorGuard-Repros
```

生成后的共享目录：

```text
/workspace/TitanFuzz/TensorGuard-Repros/logs/audit_next/queues/
```

先看队列规模：

```bash
sed -n '1,160p' TensorGuard-Repros/logs/audit_next/queues/README.md
head -n 20 TensorGuard-Repros/logs/audit_next/queues/p1_strong_crash_or_internal_assert.tsv
head -n 20 TensorGuard-Repros/logs/audit_next/queues/p2_cpu_gpu_exception_mismatch.tsv
```

## 分批审核

先跑 P1。不要一次跑很多，先从第 1 个开始跑 10 个，每个最多 60 秒：

```bash
bash TensorGuard-Repros/scripts/run_audit_queue_batch.sh \
  TensorGuard-Repros/logs/audit_next/queues/p1_strong_crash_or_internal_assert.tsv \
  1 \
  10 \
  60
```

继续跑 P1 第 11 到第 20 个：

```bash
bash TensorGuard-Repros/scripts/run_audit_queue_batch.sh \
  TensorGuard-Repros/logs/audit_next/queues/p1_strong_crash_or_internal_assert.tsv \
  11 \
  10 \
  60
```

如果 P1 候选很少，或者第一批没有新东西，再跑 P2：

```bash
bash TensorGuard-Repros/scripts/run_audit_queue_batch.sh \
  TensorGuard-Repros/logs/audit_next/queues/p2_cpu_gpu_exception_mismatch.tsv \
  1 \
  10 \
  60
```

运行日志会直接写进共享仓库目录：

```text
/workspace/TitanFuzz/TensorGuard-Repros/logs/audit_next/runs/
```

每个 batch 跑完后看这个文件：

```bash
find TensorGuard-Repros/logs/audit_next/runs -name interesting_hits.txt -print
sed -n '1,120p' TensorGuard-Repros/logs/audit_next/runs/p1_strong_crash_or_internal_assert/interesting_hits.txt
```

## 同步给本地

跑完一批后直接提交：

```bash
cd /workspace/TitanFuzz/TensorGuard-Repros
git add logs/audit_next reports scripts
git commit -m "add next audit queues and logs"
git push
```

然后告诉 Codex “推好了，读取 `logs/audit_next`”，本地只需要 pull 这个仓库就能分析结果。

## 判断标准

优先进入最小化的候选：

- 能在新进程稳定复现；
- 是内部断言、native crash、FPE、内存破坏、`Check failed`；
- 或 CPU 是正常错误、GPU 是 device-side assert；
- 不是语法错误、不是 alias 写入顺序、不是未初始化内存、不是纯数值误差。

暂时放弃或低优先级：

- 只由 `out=input` 或 transpose view alias 造成差异；
- `.resize_()` 后扩大 tensor 再读取新区域；
- `.numpy()` 之后修改 numpy 导致 CPU tensor 变了但 CUDA tensor 没变；
- `log/sqrt/pow` 导致 NaN/Inf 边界差异；
- TF32 造成卷积类数值误差。
