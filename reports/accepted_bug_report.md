# TitanFuzz-Qwen 已审核有效问题报告

更新日期：2026-06-12

本文档用于记录当前已经人工复核、可以作为项目成果收录的 PyTorch CPU/CUDA 行为不一致候选问题。后续继续审核时，新问题按本文末尾的模板追加。

## 1. 当前结论

目前建议收录 3 类有效问题候选：

| 编号 | 问题类别 | 代表 API | 结论强度 | 备注 |
|---|---|---|---|---|
| C1 | reduction API 在 aliased `out` 参数下 CPU/CUDA 输出不一致 | `torch.sum`, `torch.mean` | 强候选 | 需要注明涉及 input/output alias，维护者可能讨论是否属于未定义行为 |
| C2 | 矩阵乘相关 API 在输入输出别名场景下 CPU/CUDA 输出不一致 | `torch.Tensor.addmm_`, `torch.matmul` | 强候选 | 三次稳定复现，输出差异明显 |
| C3 | 非法输入下 CPU/CUDA 错误处理不一致 | `torch.quantile`, `torch.nanquantile`, `torch.multinomial`, `torch.poisson`, `torch.nn.BCELoss`, `torch.nn.MultiMarginLoss`, `torch.nn.functional.binary_cross_entropy`, `torch.nn.functional.embedding_bag`, `torch.nn.functional.one_hot` | 中等偏强 | CPU 抛出清晰 `RuntimeError`，CUDA 触发 device-side assert，并可能污染 CUDA 上下文 |

当前不建议把“候选数量”直接等价为 bug 数量。`trace.txt` 和 `simple_audit` 结果只能说明“值得审查”，最终可收录问题必须满足复现、定位、排除误报三个条件。

## 2. 审核判定标准

一个候选被收录，需要尽量满足：

1. 问题能稳定复现，最好三次运行结果一致。
2. 差异定位在目标 API 或最小复现中的关键 API，而不是后续 `log`、`sqrt`、`pow(0.5)` 等数值边界放大。
3. CPU/GPU 输入一致，随机数使用固定 seed 或最小复现使用常量输入。
4. 不是未初始化 Tensor、重复非法索引写入、NumPy view/拷贝语义差异、TF32 正常数值漂移等已知误报来源。
5. 对 CUDA device-side assert 类问题，CPU/GPU 必须用两个独立 Python 进程复核，不能只依赖 `torch2cuda.py --mode duel` 的同一进程结果。

## 3. 已收录问题详情

### C1. Reduction API + aliased `out` 参数导致 CPU/CUDA 输出不一致

**问题描述**

当 reduction API 的输入和 `out` 输出张量发生别名关系时，CPU 和 CUDA 后端给出不同结果。该类问题已在 `torch.sum` 和 `torch.mean` 上复现。

**来源候选**

| 来源候选 | 说明 |
|---|---|
| `Results/torch/valid/torch.Tensor.amin_1345.py` | simple audit 严格 logic output candidate |
| `Results/torch/valid/torch.Tensor.amin_1400.py` | simple audit 严格 logic output candidate |
| `Results/torch/valid/torch.diagflat_657.py` | simple audit 严格 logic output candidate |
| `Results/torch/valid/torch.mean_289.py` | 后续审核中归入同类 |
| `Results/torch/valid/torch.amin_686.py` | 后续审核中归入同类 |

**最小复现 1：`torch.sum`**

```python
import torch

def run(device):
    x = torch.ones((1, 1), device=device)
    torch.sum(x, dim=-1, keepdim=True, out=x)
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    return x.cpu()

print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("CPU:", run("cpu"))
print("GPU:", run("cuda:0"))
```

已观察结果：

```text
CPU: tensor([[0.]])
GPU: tensor([[1.]])
```

**最小复现 2：`torch.mean`**

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

已观察结果，三次稳定复现：

```text
CPU: tensor([[0.]])
GPU: tensor([[1.]])
equal: False
```

**对照实验**

当不使用 input/output alias，而是使用独立 `out` 张量时，CPU/GPU 一致：

```python
import torch

def run(device):
    x = torch.ones((1, 1), device=device)
    out = torch.empty_like(x)
    torch.sum(x, dim=-1, keepdim=True, out=out)
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    return out.cpu()

print("CPU:", run("cpu"))
print("GPU:", run("cuda:0"))
```

观察结果：

```text
CPU: tensor([[1.]])
GPU: tensor([[1.]])
equal: True
```

**收录判断**

可收录为强候选，但报告和提交 issue 时需要诚实说明：该问题发生在输入和输出存在 alias 的场景，PyTorch 维护者可能会讨论这是否属于未定义行为。不过 CPU/CUDA 行为不一致且未给出一致报错，因此仍有报告价值。

### C2. 矩阵乘相关 API + alias 场景导致 CPU/CUDA 输出不一致

**问题描述**

矩阵乘相关 API 在输入、输出或转置 view 存在别名关系时，CPU 和 CUDA 后端给出稳定不同的输出。

#### C2.1 `torch.Tensor.addmm_` alias

**来源候选**

```text
Results/torch/valid/torch.Tensor.addmm__1173.py
Results/torch/valid/torch.Tensor.addmm__1010.py
Results/torch/valid/torch.Tensor.addmm__1426.py
Results/torch/valid/torch.Tensor.addmm__1434.py
Results/torch/valid/torch.Tensor.addmm__275.py
Results/torch/valid/torch.Tensor.addmm__334.py
```

**最小复现**

```python
import torch

def run(device):
    mat1 = torch.tensor([[1.0, 2.0], [3.0, 4.0]], device=device)
    mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]], device=device)
    torch.Tensor.addmm_(mat1, mat2, mat1.transpose(0, 1))
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

已观察结果，三次稳定复现：

```text
CPU: tensor([[ 18., 156.],
             [ 26., 218.]])
GPU: tensor([[18., 41.],
             [26., 57.]])
equal: False
```

**补充复现：`torch.Tensor.addmm__1010`**

该候选同样定位在 `torch.Tensor.addmm_(mat1, mat2, mat1.t())`，属于 in-place 写入张量和转置 view 发生 alias 的场景。

最小复现：

```python
import torch

def run(device):
    mat1 = torch.tensor([
        [-5.0930,  1.9123],
        [ 0.2343, -1.2420],
    ], device=device)

    mat2 = torch.tensor([
        [5.0, 6.0],
        [7.0, 8.0],
    ], device=device)

    torch.Tensor.addmm_(mat1, mat2, mat1.t())

    if device.startswith("cuda"):
        torch.cuda.synchronize()

    return mat1.detach().cpu()

cpu = run("cpu")
gpu = run("cuda:0")

print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("CPU:", cpu)
print("GPU:", gpu)
print("equal:", torch.equal(cpu, gpu))

assert torch.equal(cpu, gpu), (cpu, gpu)
```

已观察结果：三次运行均 CPU/GPU 不一致。该样例作为 C2 的补充来源证据，不单独新建类别。

**补充来源证据：更多 `addmm_` alias 变体**

以下候选均已由 `torch2cuda.py --mode duel` 定位到 `torch.Tensor.addmm_(...)` 调用本身，且最终 `mat1` 或其别名 view 在 CPU/CUDA 上稳定不一致：

| 来源候选 | 触发形式 | CPU/GPU 差异概述 |
|---|---|---|
| `Results/torch/valid/torch.Tensor.addmm__1426.py` | `torch.Tensor.addmm_(mat1, mat2, mat1.t())` | CPU `mat1` 为 `[[18,173],[28,241]]`，GPU 为 `[[18,53],[28,73]]` |
| `Results/torch/valid/torch.Tensor.addmm__1434.py` | `torch.Tensor.addmm_(mat1, mat1, mat2.t())` | CPU `mat1` 为 `[[18,144],[50.4,397.8]]`，GPU 为 `[[18,25],[50.4,68.8]]` |
| `Results/torch/valid/torch.Tensor.addmm__275.py` | `torch.Tensor.addmm_(mat1.t(), mat2, torch.transpose(mat1, 0, 1))` | CPU `mat1` 为 `[[18,144],[18,126]]`，GPU 为 `[[18,25],[18,21]]` |
| `Results/torch/valid/torch.Tensor.addmm__334.py` | `torch.Tensor.addmm_(mat1.t(), mat1, mat2.t())` | CPU `mat1` 为 `[[18,156],[26,218]]`，GPU 为 `[[18,41],[26,57]]` |

这些样例不单独新建问题类别，统一归入 C2：矩阵乘相关 API 在输入输出别名场景下 CPU/CUDA 输出不一致。

#### C2.2 `torch.matmul(..., out=x)` alias

**来源候选**

```text
Results/torch/valid/torch.Tensor.t_407.py
```

**最小复现**

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

已观察结果，三次稳定复现：

```text
CPU: tensor([[ 1.7805e+01, -2.2633e+02, -2.7936e+01],
             [-1.2417e+01,  1.6180e+02,  1.9933e+01],
             [-2.8201e+01,  3.6875e+02,  1.3677e+05]])
GPU: tensor([[ 17.8045, -12.4165,  -0.6808],
             [-12.4165,  11.2403,   0.5489],
             [ -0.6808,   0.5489,   0.0282]])
equal: False
```

**收录判断**

可收录为强候选。与 C1 类似，该问题也涉及 alias 场景，需要在报告中注明。优势是输出差异非常明显，并且多次运行稳定。

### C3. 非法输入下 CPU/CUDA 错误处理不一致

**问题描述**

多个 API 在非法输入下，CPU 后端会抛出清晰、可恢复的 `RuntimeError`，而 CUDA 后端进入 kernel 后触发 `device-side assert`。这会导致错误信息不一致，并可能污染当前 CUDA 上下文，使后续 CUDA 调用继续失败。

这类问题不是“正常输入计算错误”，而是错误处理/输入校验一致性问题。

**复核要求**

该类问题必须 CPU 和 GPU 分开跑两个独立 Python 进程。例如：

```bash
python repro_xxx.py cpu
CUDA_LAUNCH_BLOCKING=1 python repro_xxx.py cuda:0
```

不能只依赖 `torch2cuda.py --mode duel` 的同一进程结果，因为 CUDA device-side assert 之后，同一进程的 CPU/GPU 对照可能被污染。

#### C3.1 `torch.quantile`

**现象**

非法 `q` 值超出 `[0, 1]` 范围。

已观察结果：

```text
CPU:
RuntimeError: quantile() q values must be in the range [0, 1]

GPU:
torch.AcceleratorError: CUDA error: device-side assert triggered
```

**收录判断**

可收录，归入 C3。

#### C3.2 `torch.nanquantile`

**来源候选**

```text
Results/torch/exception/torch.Tensor.nanquantile_206.py
```

**现象**

非法 `q` 值，例如 `torch.tensor([1.0, 2.5])`。

已观察结果：

```text
CPU:
RuntimeError: quantile() q values must be in the range [0, 1]

GPU:
torch.AcceleratorError: CUDA error: device-side assert triggered
```

**收录判断**

可收录，归入 C3。

#### C3.3 `torch.multinomial`

**来源候选**

```text
Results/torch/exception/torch.multinomial_1019.py
```

**现象**

输入概率分布非法，例如概率和小于等于 0。

已观察结果：

```text
CPU:
RuntimeError: invalid multinomial distribution (sum of probabilities <= 0)

GPU:
CUDA device-side assert
```

**收录判断**

可收录，归入 C3。

#### C3.4 `torch.poisson`

**来源候选**

```text
Results/torch/exception/torch.poisson_112.py
```

**现象**

输入 rate 非法，例如负数或由 `log(0)` 得到的非法值。

已观察结果：

```text
CPU:
RuntimeError: invalid Poisson rate, expected rate to be non-negative

GPU:
CUDA device-side assert
```

**收录判断**

可收录，归入 C3。

#### C3.5 `torch.nn.BCELoss`

**来源候选**

```text
Results/torch/exception/torch.nn.BCELoss_262.py
```

**现象**

输入或 target 超出 BCE 约束范围。

已观察结果：

```text
CPU:
RuntimeError: all elements of input should be between 0 and 1

GPU:
CUDA device-side assert
```

**收录判断**

可收录，归入 C3。

#### C3.6 `torch.nn.MultiMarginLoss`

**来源候选**

```text
Results/torch/exception/torch.nn.MultiMarginLoss_589.py
```

**最小复现**

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

复现命令：

```bash
python repro_multimargin_invalid_target.py cpu
CUDA_LAUNCH_BLOCKING=1 python repro_multimargin_invalid_target.py cuda:0
```

已观察结果：

```text
CPU:
RuntimeError: target out of range

GPU:
torch.AcceleratorError: CUDA error: device-side assert triggered
```

**收录判断**

可收录，归入 C3。该结果由 CPU/GPU 独立进程复核，不属于 `torch2cuda.py` 同进程污染。

#### C3.7 `torch.nn.functional.binary_cross_entropy`

**来源候选**

```text
Results/torch/exception/torch.nn.functional.binary_cross_entropy_1505.py
```

**最小复现**

```python
import torch
import torch.nn.functional as F

device = "cuda:0"  # 或 "cpu"
x = torch.full((2, 2), 2.0, device=device)
target = torch.ones((2, 2), device=device)

y = F.binary_cross_entropy(x, target)

if device.startswith("cuda"):
    torch.cuda.synchronize()

print(y)
```

**已观察结果**

```text
CPU:
RuntimeError: all elements of input should be between 0 and 1

GPU:
torch.AcceleratorError: CUDA error: device-side assert triggered
```

**收录判断**

可收录，归入 C3。这和 `torch.nn.BCELoss` 属于同一底层问题族，但可作为 functional API 的独立证据。

#### C3.8 `torch.nn.functional.embedding_bag`

**来源候选**

```text
Results/torch/exception/torch.nn.functional.embedding_bag_1011.py
```

**最小复现**

```python
import torch
import torch.nn.functional as F

device = "cuda:0"  # 或 "cpu"
weight = torch.randn(4, 3, device=device)
indices = torch.tensor([0, 1, 4], dtype=torch.long, device=device)
offsets = torch.tensor([0], dtype=torch.long, device=device)

y = F.embedding_bag(indices, weight, offsets, mode="sum")

if device.startswith("cuda"):
    torch.cuda.synchronize()

print(y)
```

**已观察结果**

```text
CPU:
RuntimeError: Index 2 of input takes value 4 which is not in the valid range [0, 4)

GPU:
torch.AcceleratorError: CUDA error: device-side assert triggered
```

**收录判断**

可收录，归入 C3。该问题表现为越界 index 在 CPU 上被清晰检查，在 CUDA 上进入 kernel 后触发 device-side assert。

#### C3.9 `torch.nn.functional.one_hot`

**来源候选**

```text
Results/torch/exception/torch.nn.functional.soft_margin_loss_1329.py
```

**说明**

原候选来自 `soft_margin_loss` 路径，但独立复核后，最小根因定位在前置的 `torch.nn.functional.one_hot`，不是 `soft_margin_loss` 本身。

**最小复现**

```python
import torch
import torch.nn.functional as F

device = "cuda:0"  # 或 "cpu"
x = torch.tensor([[0, 0], [-1, 0]], dtype=torch.long, device=device)

y = F.one_hot(x, num_classes=2)

if device.startswith("cuda"):
    torch.cuda.synchronize()

print(y)
```

**已观察结果**

```text
CPU:
RuntimeError: Class values must be non-negative.

GPU:
torch.AcceleratorError: CUDA error: device-side assert triggered
```

**收录判断**

可收录，归入 C3。注意对外报告时应写 `torch.nn.functional.one_hot`，不要写成 `soft_margin_loss` bug。

## 4. 已审核但暂不收录的问题

以下问题已经审核过，当前不建议作为有效 bug 收录：

| 候选 | 不收原因 |
|---|---|
| `torch.nn.functional.conv3d_1028` | 关闭 TF32 后差异降至正常浮点误差范围，属于 TF32 numeric drift |
| `torch.nn.functional.conv_transpose3d_165` | 关闭 TF32 后 `allclose 1e-5/1e-5=True`，属于 TF32 numeric drift |
| `torch.Tensor.addcdiv_153` | CPU `.numpy()` 共享内存，GPU 路径经工具转换/拷贝，属于 NumPy view/转换语义差异 |
| `max_unpool1d_1` / `torch.nn.MaxUnpool2d_1138` 类 | indices 为手造重复/非法索引，存在写入冲突，不适合作为强 bug |
| `torch.Tensor.argsort_179` | 重复值排序稳定性不保证，最终输出一致或差异不干净 |
| `torch.Tensor.broadcast_to_919` | broadcast view + `.to("cpu")` 语义差异，不适合作为框架 bug |
| `torch.Tensor.logical_not_1150` | 使用 `torch.empty_like` 未初始化内存，属于伪阳性 |
| `torch.Tensor.mv_625` | 差异来自 `torch.Tensor(result.size())` 未初始化 Tensor，不收 |
| `torch.nn.BatchNorm3d_1001` | 差异不是目标输出，且后续包含数值边界放大操作 |
| `torch.nn.MultiheadAttention_717` | 使用 `torch.FloatTensor(size)` 未初始化 Tensor，不收 |
| `torch.Tensor.put__100` | 重复 index 且 `accumulate=False`，写入顺序不适合作为强 bug |
| `torch.Tensor.floor_divide__140` | 差异来自 `exp/log` 后靠近整数边界，再被 `torch.floor` 放大；`floor_divide_` 只是对已经分叉的值除以 1，不是目标 API bug |
| `torch.Tensor.renorm__1134` | `DuelFinished` 定位在 `torch.Tensor.resize_` 扩容，新增区域包含未初始化内存，不是 `renorm_` 本身问题 |
| `torch.Tensor.floor_divide_391` | `sqrt(input_tensor)` 与 `sqrt(input_tensor + 1e-07)` 极接近，`floor_divide` 在 1 附近的边界把正常浮点差异放大成 0/1，不适合作为框架 bug |
| `torch.nn.functional.binary_cross_entropy_with_logits_22` / `bce_with_logits_invalid_target` | CPU/GPU 独立进程均正常返回，不存在异常不一致 |
| `torch.nn.FractionalMaxPool3d_1272` / `fractional_max_pool3d_invalid_output_size` | CPU/GPU 均抛出相同 `RuntimeError`，不是 CPU/CUDA 错误处理不一致 |

## 5. 后续追加模板

每新增一个可收录候选，按如下格式追加。

````markdown
### Cx.y API 名称

**来源候选**

```text
Results/torch/...
```

**问题类别**

```text
C1 / C2 / C3 / 新类别
```

**最小复现**

```python
# 放最小代码
```

**复现命令**

```bash
# 放命令
```

**CPU 结果**

```text
# 放 CPU 输出
```

**GPU 结果**

```text
# 放 GPU 输出
```

**稳定性**

```text
是否三次稳定复现：
```

**收录判断**

```text
可收 / 暂不收 / 需要继续最小化
```

**备注**

```text
是否涉及 alias、非法输入、数值边界、TF32、未初始化 Tensor、重复索引等。
```
````

## 6. 对外表述建议

建议在 PPT、项目报告或 GitHub README 中这样描述：

```text
我们基于 TitanFuzz 的 API fuzzing 流程，引入本地 Qwen 生成/修复种子程序，并对 PyTorch CPU/CUDA 后端行为进行差分测试。经过 trace 解析、候选去重、复现验证和人工最小化，目前确认了三类可复现的 PyTorch 行为不一致候选问题：reduction API 在 aliased out 参数下 CPU/CUDA 输出不一致、矩阵乘相关 API 在输入输出别名场景下输出不一致，以及多个 API 在非法输入下 CPU/CUDA 错误处理不一致。
```

更谨慎的措辞：

```text
这些结果是有效 bug candidates，尚未全部经过 PyTorch 官方确认。我们已为每类问题提供最小复现、CPU/GPU 对照输出和误报过滤依据。
```
