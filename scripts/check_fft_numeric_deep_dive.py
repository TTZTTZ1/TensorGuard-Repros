#!/usr/bin/env python3
"""Deep-dive FFT numeric mismatches that failed loose allclose checks.

Run from the TitanFuzz root on the GPU server:

  python TensorGuard-Repros/scripts/check_fft_numeric_deep_dive.py \
    > TensorGuard-Repros/logs/trace_logic_review/repro_logs/p2_remaining_numeric_next30_txt/fft_numeric_deep_dive.txt 2>&1
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import torch


TensorFn = Callable[[str, torch.dtype], torch.Tensor]


@dataclass(frozen=True)
class Case:
    name: str
    fn: TensorFn


def hfft_570(device: str, dtype: torch.dtype) -> torch.Tensor:
    return torch.fft.hfft(torch.arange(0, 1024, 0.1, dtype=dtype, device=device))


def hfft_779(device: str, dtype: torch.dtype) -> torch.Tensor:
    return torch.fft.hfft(torch.arange(2**13, dtype=dtype, device=device))


def hfft_782(device: str, dtype: torch.dtype) -> torch.Tensor:
    x = torch.arange(2**13, dtype=dtype, device=device).view(1, 2**13)
    return torch.fft.hfft(x)


def ihfft_1268(device: str, dtype: torch.dtype) -> torch.Tensor:
    x = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=dtype, device=device)
    result = torch.fft.ihfft(x)
    result = torch.fft.ifft(result)
    result = torch.fft.fft(result, n=2048)
    result = torch.fft.hfft(result, n=2048)
    result = torch.fft.hfft(result, n=2048)
    return torch.fft.hfft(result, n=1024)


def ihfft_773(device: str, dtype: torch.dtype) -> torch.Tensor:
    x = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=dtype, device=device)
    result = torch.fft.ihfft(x)
    result = torch.fft.fft(result, n=2048)
    result = torch.fft.fft(result, n=2048)
    result = torch.fft.fft(result, n=2048)
    return torch.fft.fft(result, n=2048)


CASES = [
    Case("torch.fft.hfft_570", hfft_570),
    Case("torch.fft.hfft_779", hfft_779),
    Case("torch.fft.hfft_782", hfft_782),
    Case("torch.fft.ihfft_1268", ihfft_1268),
    Case("torch.fft.ihfft_773", ihfft_773),
]


def flatten_index(index: int, shape: tuple[int, ...]) -> tuple[int, ...]:
    coords = []
    for size in reversed(shape):
        coords.append(index % size)
        index //= size
    return tuple(reversed(coords))


def report(case: Case, dtype: torch.dtype) -> None:
    with torch.no_grad():
        cpu = case.fn("cpu", dtype).detach().cpu()
        gpu = case.fn("cuda:0", dtype)
        torch.cuda.synchronize()
        gpu = gpu.detach().cpu()

    cpu_finite = torch.isfinite(cpu)
    gpu_finite = torch.isfinite(gpu)
    common = cpu_finite & gpu_finite
    diff = (cpu[common] - gpu[common]).abs()
    cpu_common = cpu[common]
    gpu_common = gpu[common]

    print(f"case={case.name} dtype={dtype}")
    print(f"shape={tuple(cpu.shape)} result_dtype={cpu.dtype}")
    print(f"finite_mask_equal={torch.equal(cpu_finite, gpu_finite)}")
    print(f"common_finite={common.sum().item()}/{cpu.numel()}")

    if not common.any():
        print("no_common_finite_values=True")
        print()
        return

    max_idx = int(diff.argmax().item())
    flat_cpu = cpu_common.flatten()
    flat_gpu = gpu_common.flatten()
    flat_diff = diff.flatten()
    original_flat_indices = common.flatten().nonzero().flatten()
    original_flat = int(original_flat_indices[max_idx].item())
    coords = flatten_index(original_flat, tuple(cpu.shape))

    cpu_norm = torch.linalg.vector_norm(cpu_common.flatten()).item()
    gpu_norm = torch.linalg.vector_norm(gpu_common.flatten()).item()
    diff_norm = torch.linalg.vector_norm(diff.flatten()).item()
    denom = max(cpu_norm, gpu_norm, 1e-30)

    print(f"max_abs={flat_diff[max_idx].item():.12g}")
    print(f"mean_abs={diff.mean().item():.12g}")
    print(f"l2_rel={diff_norm / denom:.12g}")
    print(f"cpu_norm={cpu_norm:.12g}")
    print(f"gpu_norm={gpu_norm:.12g}")
    print(f"max_index={coords}")
    print(f"cpu_at_max={flat_cpu[max_idx]}")
    print(f"gpu_at_max={flat_gpu[max_idx]}")
    for tol in (1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
        ok = torch.allclose(cpu_common, gpu_common, rtol=tol, atol=tol)
        print(f"allclose_{tol:g}={ok}")
    print()


def main() -> None:
    print("torch:", torch.__version__)
    print("cuda:", torch.version.cuda)
    if not torch.cuda.is_available():
        raise SystemExit("CUDA is not available")
    print("device:", torch.cuda.get_device_name(0))
    print()

    for case in CASES:
        for dtype in (torch.float32, torch.float64):
            report(case, dtype)


if __name__ == "__main__":
    main()
