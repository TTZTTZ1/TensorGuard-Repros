# PyTorch CPU/CUDA 行为不一致问题阶段性总结

更新日期：2026-06-12

## 0. 总览

目前人工复核后，建议保留：

```text
3 类问题根因
18 条可复现样例 / API 证据
```

不要直接表述为“18 个完全独立 bug”。更稳妥的说法是：

```text
目前确认 3 类 PyTorch CPU/CUDA 行为不一致候选问题，覆盖 18 个可复现样例/API 证据。
```

当前主要环境：

```text
PyTorch 2.11.0+cu130
CUDA 13.0
```

部分早期样例曾在：

```text
PyTorch 2.10.0+cu128
CUDA 12.8
```

后续若要提交 PyTorch issue，建议统一在最终环境重跑并保存日志。

## 1. C1：Reduction API 在 aliased out 参数下 CPU/CUDA 输出不一致

### 问题描述

当 reduction API 的输入 tensor 和 `out` 输出 tensor 是同一个对象时，CPU 和 CUDA 后端给出不同结果。

已确认代表：

```text
torch.sum
torch.mean
```

### 最小复现：torch.mean

```python
import torch

def run(device):
    x = torch.ones((1, 1), device=device)
    torch.mean(x, dim=-1, keepdim=True, out=x)
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    return x.cpu()

cpu = run("cpu")
gpu = run("cuda:0")

print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("CPU:", cpu)
print("GPU:", gpu)
print("equal:", torch.equal(cpu, gpu))

assert torch.equal(cpu, gpu), (cpu, gpu)
```

观察结果：

```text
CPU: tensor([[0.]])
GPU: tensor([[1.]])
equal: False
```

### 对照实验

如果使用独立 `out` tensor，CPU/GPU 一致：

```python
import torch

def run(device):
    x = torch.ones((1, 1), device=device)
    out = torch.empty_like(x)
    torch.mean(x, dim=-1, keepdim=True, out=out)
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    return out.cpu()

print("CPU:", run("cpu"))
print("GPU:", run("cuda:0"))
```

预期/观察：

```text
CPU: tensor([[1.]])
GPU: tensor([[1.]])
```

### 初步原因判断

该问题与 input/output alias 有关。CPU 与 CUDA 在 reduction 写回 `out` 时，对读写顺序或 alias 处理策略不一致。

谨慎表述：

```text
Reduction kernels do not consistently handle aliased input/output tensors across CPU and CUDA backends.
```

注意：该类问题涉及 alias，PyTorch 维护者可能讨论这种用法是否属于未定义行为，但 CPU/CUDA 行为不一致且没有一致报错，因此仍有报告价值。

## 2. C2：矩阵乘相关 API 在 alias 场景下 CPU/CUDA 输出不一致

### 问题描述

当矩阵乘相关 API 的输出 tensor 和输入 tensor 的 view 共享底层存储时，CPU 和 CUDA 后端输出不同。

已确认代表：

```text
torch.Tensor.addmm_
torch.matmul(..., out=...)
```

目前 C2 下已有 7 条证据，其中 `addmm_` 多个变体均定位到同一类根因。

### 最小复现：torch.Tensor.addmm_

```python
import torch

def run(device):
    mat1 = torch.tensor([[1.0, 2.0], [3.0, 4.0]], device=device)
    mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]], device=device)

    # mat1 是被原地写入的 tensor，mat1.t() 是 mat1 的转置 view。
    # 二者共享底层存储。
    torch.Tensor.addmm_(mat1, mat2, mat1.t())

    if device.startswith("cuda"):
        torch.cuda.synchronize()

    return mat1.cpu()

cpu = run("cpu")
gpu = run("cuda:0")

print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("CPU:", cpu)
print("GPU:", gpu)
print("equal:", torch.equal(cpu, gpu))

assert torch.equal(cpu, gpu), (cpu, gpu)
```

观察结果：

```text
CPU:
tensor([[ 18., 156.],
        [ 26., 218.]])

GPU:
tensor([[18., 41.],
        [26., 57.]])

equal: False
```

### 最小复现：torch.matmul out alias

```python
import torch

def run(device):
    x = torch.tensor([
        [-1.6977,  0.6374,  0.0781],
        [-0.4140,  1.5172,  0.0473],
        [ 0.8435, -0.2261,  0.0345],
    ], device=device)

    y = x.t()
    torch.matmul(y, x, out=x)
    torch.matmul(x, y, out=x)

    if device.startswith("cuda"):
        torch.cuda.synchronize()

    return x.cpu()

cpu = run("cpu")
gpu = run("cuda:0")

print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("CPU:", cpu)
print("GPU:", gpu)
print("equal:", torch.equal(cpu, gpu))

assert torch.equal(cpu, gpu), (cpu, gpu)
```

观察结果：

```text
CPU:
tensor([[ 1.7805e+01, -2.2633e+02, -2.7936e+01],
        [-1.2417e+01,  1.6180e+02,  1.9933e+01],
        [-2.8201e+01,  3.6875e+02,  1.3677e+05]])

GPU:
tensor([[ 17.8045, -12.4165,  -0.6808],
        [-12.4165,  11.2403,   0.5489],
        [ -0.6808,   0.5489,   0.0282]])

equal: False
```

### 补充证据

以下 `addmm_` 样例均定位到 `torch.Tensor.addmm_(...)` 本身，最终 `mat1` CPU/GPU 不一致：

```text
Results/torch/valid/torch.Tensor.addmm__1173.py
Results/torch/valid/torch.Tensor.addmm__1010.py
Results/torch/valid/torch.Tensor.addmm__1426.py
Results/torch/valid/torch.Tensor.addmm__1434.py
Results/torch/valid/torch.Tensor.addmm__275.py
Results/torch/valid/torch.Tensor.addmm__334.py
```

### 初步原因判断

该问题与矩阵乘操作中的 alias/write-order 有关。输出 tensor 与输入 tensor 的 transpose view 共享底层存储，CPU 与 CUDA 的读写顺序或 kernel alias 处理策略不同，导致结果分叉。

谨慎表述：

```text
Matrix multiplication kernels produce inconsistent results when the output tensor aliases one of the input operands through a view such as transpose.
```

同样需要注意：该问题涉及 alias 场景，是否属于 PyTorch 明确定义行为需要维护者进一步确认。但从差分测试角度看，CPU/CUDA 后端行为不一致，且结果差异稳定、明显。

## 3. C3：非法输入下 CPU/CUDA 错误处理不一致

### 问题描述

多个 API 在非法输入下，CPU 后端会抛出清晰的 `RuntimeError`，而 CUDA 后端进入 kernel 后触发 `device-side assert`。这会导致：

```text
1. CPU/CUDA 错误类型和错误信息不一致；
2. CUDA device-side assert 可能污染当前 CUDA 上下文；
3. 同一进程中后续 CUDA 调用可能继续失败。
```

该类不是“正常输入计算错误”，而是输入校验/错误处理一致性问题。

已确认代表：

```text
torch.quantile
torch.nanquantile
torch.multinomial
torch.poisson
torch.nn.BCELoss
torch.nn.MultiMarginLoss
torch.nn.functional.binary_cross_entropy
torch.nn.functional.embedding_bag
torch.nn.functional.one_hot
```

注意：这类必须 CPU/GPU 独立进程复核，不能只依赖 `torch2cuda.py --mode duel` 的同一进程结果。

### 最小复现：embedding_bag invalid index

```python
import sys
import torch
import torch.nn.functional as F

device = sys.argv[1]
print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("device:", device)

weight = torch.randn(4, 3, device=device)
indices = torch.tensor([0, 1, 4], dtype=torch.long, device=device)
offsets = torch.tensor([0], dtype=torch.long, device=device)

y = F.embedding_bag(indices, weight, offsets, mode="sum")

if device.startswith("cuda"):
    torch.cuda.synchronize()

print(y)
```

运行：

```bash
python repro_embedding_bag_invalid_index.py cpu
CUDA_LAUNCH_BLOCKING=1 python repro_embedding_bag_invalid_index.py cuda:0
```

观察结果：

```text
CPU:
RuntimeError: Index 2 of input takes value 4 which is not in the valid range [0, 4)

GPU:
torch.AcceleratorError: CUDA error: device-side assert triggered
```

### 最小复现：one_hot negative class

```python
import sys
import torch
import torch.nn.functional as F

device = sys.argv[1]
print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("device:", device)

x = torch.tensor([[0, 0], [-1, 0]], dtype=torch.long, device=device)

y = F.one_hot(x, num_classes=2)

if device.startswith("cuda"):
    torch.cuda.synchronize()

print(y)
```

运行：

```bash
python repro_one_hot_negative_class.py cpu
CUDA_LAUNCH_BLOCKING=1 python repro_one_hot_negative_class.py cuda:0
```

观察结果：

```text
CPU:
RuntimeError: Class values must be non-negative.

GPU:
torch.AcceleratorError: CUDA error: device-side assert triggered
```

### 最小复现：MultiMarginLoss invalid target

```python
import sys
import torch

device = sys.argv[1]
print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("device:", device)

input = torch.randn(3, device=device)
target = torch.tensor(20, device=device)

loss_fn = torch.nn.MultiMarginLoss()
y = loss_fn(input.unsqueeze(0), target.unsqueeze(0))

if device.startswith("cuda"):
    torch.cuda.synchronize()

print(y)
```

运行：

```bash
python repro_multimargin_invalid_target.py cpu
CUDA_LAUNCH_BLOCKING=1 python repro_multimargin_invalid_target.py cuda:0
```

观察结果：

```text
CPU:
RuntimeError: target out of range

GPU:
torch.AcceleratorError: CUDA error: device-side assert triggered
```

### 初步原因判断

CPU 后端通常在执行前或执行过程中给出清晰的输入校验错误；CUDA 后端部分路径缺少一致的前置校验，非法输入进入 kernel 后触发 device-side assert。

谨慎表述：

```text
Some CUDA kernels lack the same pre-dispatch input validation as CPU kernels. Invalid inputs are caught as clean RuntimeError on CPU, but trigger device-side assertions on CUDA.
```

## 4. 已排除的典型误报

审核过程中已排除多类误报，避免把普通数值差异或生成代码问题误判为 bug：

```text
1. TF32 数值漂移：
   conv3d / conv_transpose3d 关闭 TF32 后 allclose 通过。

2. 未初始化内存：
   resize_ 扩容、torch.empty_like、torch.Tensor(size) 等。

3. 数值边界放大：
   log / sqrt / floor / exp 等把普通浮点误差放大成 nan、inf 或 0/1。

4. 重复非法索引写入：
   put_、max_unpool 等手造重复 index。

5. NumPy view / GPU 拷贝语义差异：
   CPU tensor.numpy() 共享内存，GPU 路径经转换/拷贝。
```

这部分可以作为作品的“误报过滤与人工复核标准”。

## 5. 建议给学长的评估问题

可以请学长重点评估：

```text
1. C1/C2 这类 alias 场景是否值得作为 PyTorch issue 提交？
2. C3 这类非法输入下 CPU/CUDA 错误处理不一致，是否算有价值的框架鲁棒性 bug？
3. 对比赛展示而言，是按 3 类根因展示，还是按 18 条可复现样例展示？
4. 哪些样例最适合作为最终答辩现场演示？
```

我个人建议最终展示时按“3 类根因 + 若干代表样例”组织，而不是堆 18 条列表。

