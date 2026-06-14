#!/usr/bin/env python3
"""Independently check the P2 conv3d CPU/CUDA numeric candidates.

Run from the TitanFuzz root on the GPU server:

  python TensorGuard-Repros/scripts/check_conv3d_numeric_batch.py \
    > TensorGuard-Repros/logs/trace_logic_review/repro_logs/p2_conv_ctc_first30_txt/conv3d_numeric_independent.txt 2>&1

The TitanFuzz logs only say that the output tensors differ.  This script
recreates the source-level conv3d calls with identical CPU/GPU inputs and
reports numerical error with TF32 enabled and disabled.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import torch
import torch.nn.functional as F


@dataclass(frozen=True)
class Conv3dCase:
    name: str
    input_shape: tuple[int, int, int, int, int]
    weight_shape: tuple[int, int, int, int, int]
    kwargs: dict[str, Any]
    requires_grad: bool = False


CASES = [
    Conv3dCase(
        "torch.nn.functional.conv3d_1",
        (1, 16, 32, 32, 32),
        (8, 16, 5, 5, 5),
        {},
    ),
    Conv3dCase(
        "torch.nn.functional.conv3d_1028",
        (1, 16, 32, 32, 32),
        (8, 16, 3, 3, 3),
        {},
        requires_grad=True,
    ),
    Conv3dCase(
        "torch.nn.functional.conv3d_1134",
        (1, 16, 32, 32, 32),
        (8, 16, 3, 3, 3),
        {},
        requires_grad=True,
    ),
    Conv3dCase(
        "torch.nn.functional.conv3d_1136",
        (1, 16, 32, 32, 32),
        (8, 16, 3, 3, 3),
        {"stride": 3, "padding": 1, "dilation": 1, "groups": 1},
        requires_grad=True,
    ),
    Conv3dCase(
        "torch.nn.functional.conv3d_1147",
        (1, 16, 32, 32, 32),
        (8, 16, 3, 3, 3),
        {"stride": (1, 1, 1), "padding": (0,)},
        requires_grad=True,
    ),
    Conv3dCase(
        "torch.nn.functional.conv3d_1192",
        (1, 16, 32, 32, 32),
        (8, 16, 3, 3, 3),
        {"stride": (1, 1, 1), "padding": 1},
        requires_grad=True,
    ),
    Conv3dCase(
        "torch.nn.functional.conv3d_1203",
        (1, 16, 32, 32, 32),
        (8, 16, 3, 3, 3),
        {"stride": 1, "padding": (3, 3, 3), "dilation": (3, 3, 3)},
        requires_grad=True,
    ),
    Conv3dCase(
        "torch.nn.functional.conv3d_1204",
        (1, 16, 32, 32, 32),
        (8, 16, 3, 3, 3),
        {"stride": 2, "padding": 1, "dilation": 1},
        requires_grad=True,
    ),
    Conv3dCase(
        "torch.nn.functional.conv3d_1235",
        (1, 16, 32, 32, 32),
        (8, 16, 3, 3, 3),
        {"padding": (3, 3, 3), "stride": (1, 1, 1)},
        requires_grad=True,
    ),
    Conv3dCase(
        "torch.nn.functional.conv3d_1245",
        (1, 16, 32, 32, 32),
        (8, 16, 3, 3, 3),
        {"padding": (3, 3, 3), "groups": 1},
        requires_grad=True,
    ),
]


def set_tf32(enabled: bool) -> None:
    torch.backends.cudnn.allow_tf32 = enabled
    torch.backends.cuda.matmul.allow_tf32 = enabled
    torch.backends.cudnn.benchmark = False


def rel_error(cpu: torch.Tensor, gpu: torch.Tensor) -> float:
    denom = torch.maximum(cpu.abs(), torch.full_like(cpu, 1e-12))
    rel = (cpu - gpu).abs() / denom
    value = rel.max().item()
    return value if math.isfinite(value) else float("inf")


def run_case(case: Conv3dCase, tf32: bool) -> None:
    set_tf32(tf32)
    torch.manual_seed(420)

    x_cpu = torch.randn(case.input_shape, dtype=torch.float32)
    w_cpu = torch.randn(case.weight_shape, dtype=torch.float32)
    b_cpu = torch.randn(case.weight_shape[0], dtype=torch.float32)
    if case.requires_grad:
        x_cpu.requires_grad_(True)

    with torch.no_grad():
        y_cpu = F.conv3d(x_cpu, w_cpu, b_cpu, **case.kwargs).detach().cpu()

        x_gpu = x_cpu.detach().to("cuda:0")
        w_gpu = w_cpu.to("cuda:0")
        b_gpu = b_cpu.to("cuda:0")
        y_gpu = F.conv3d(x_gpu, w_gpu, b_gpu, **case.kwargs)
        torch.cuda.synchronize()
        y_gpu = y_gpu.detach().cpu()

    diff = (y_cpu - y_gpu).abs()
    print(f"case={case.name} tf32={tf32}")
    print(f"shape={tuple(y_cpu.shape)}")
    print(f"max_abs={diff.max().item():.9g}")
    print(f"mean_abs={diff.mean().item():.9g}")
    print(f"max_rel={rel_error(y_cpu, y_gpu):.9g}")
    print(f"allclose_1e-5={torch.allclose(y_cpu, y_gpu, rtol=1e-5, atol=1e-5)}")
    print(f"allclose_1e-4={torch.allclose(y_cpu, y_gpu, rtol=1e-4, atol=1e-4)}")
    print(f"allclose_1e-3={torch.allclose(y_cpu, y_gpu, rtol=1e-3, atol=1e-3)}")
    print()


def main() -> None:
    print("torch:", torch.__version__)
    print("cuda:", torch.version.cuda)
    if not torch.cuda.is_available():
        raise SystemExit("CUDA is not available")
    print("device:", torch.cuda.get_device_name(0))
    print()

    for tf32 in (True, False):
        print(f"===== TF32 {tf32} =====")
        for case in CASES:
            run_case(case, tf32)


if __name__ == "__main__":
    main()
