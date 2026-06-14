#!/usr/bin/env python3
"""Independently check representative P2 FFT CPU/CUDA numeric candidates.

Run from the TitanFuzz root on the GPU server:

  python TensorGuard-Repros/scripts/check_fft_numeric_batch.py \
    > TensorGuard-Repros/logs/trace_logic_review/repro_logs/p2_remaining_numeric_next30_txt/fft_numeric_independent.txt 2>&1

The TitanFuzz logs show raw tensor differences for FFT-heavy programs.  This
script reruns representative source-level cases with identical CPU/GPU inputs
and reports finite masks plus tolerance-aware numerical differences.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import torch


TensorFn = Callable[[str], torch.Tensor]


@dataclass(frozen=True)
class Case:
    name: str
    fn: TensorFn


def hfft_570(device: str) -> torch.Tensor:
    fft_data = torch.arange(0, 1024, 0.1, device=device)
    return torch.fft.hfft(fft_data)


def hfft_779(device: str) -> torch.Tensor:
    fft_data = torch.arange(2**13, device=device)
    return torch.fft.hfft(fft_data)


def hfft_782(device: str) -> torch.Tensor:
    fft_data = torch.arange(2**13, device=device).view(1, 2**13)
    return torch.fft.hfft(fft_data)


def ifftn_1255(device: str) -> torch.Tensor:
    x = torch.arange(2**16, device=device).view(2, -1).type(torch.float32)
    result = torch.fft.fftshift(torch.fft.fft(x))
    result = torch.fft.ifft(result)
    result = torch.fft.fftshift(result)
    result = torch.fft.ifft(result)
    result = torch.fft.ifftn(result)
    return result


def ihfft_1059(device: str) -> torch.Tensor:
    result = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=device)
    result.requires_grad_(True)
    result = torch.fft.ihfft(result, n=2048)
    for _ in range(4):
        result = torch.fft.fft(result, n=2048)
    return result


def ihfft_1268(device: str) -> torch.Tensor:
    result = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=device)
    result.requires_grad_(True)
    result = torch.fft.ihfft(result)
    result = torch.fft.ifft(result)
    result = torch.fft.fft(result, n=2048)
    result = torch.fft.hfft(result, n=2048)
    result = torch.fft.hfft(result, n=2048)
    result.requires_grad_(True)
    return torch.fft.hfft(result, n=1024)


def ihfft_1400(device: str) -> torch.Tensor:
    result = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=device)
    result.requires_grad_(True)
    result = torch.fft.ihfft(result)
    result = torch.fft.irfft(result, n=1024)
    result = torch.fft.hfft(result, n=2048)
    result = torch.fft.irfft(result, n=1024)
    result = torch.fft.hfft(result, n=2048)
    result = torch.fft.irfft(result, n=2048)
    result = torch.fft.hfft(result, n=2048)
    result = torch.fft.hfft(result, n=2048)
    result = torch.fft.hfft(result, n=1024)
    result.requires_grad_(True)
    result = torch.fft.fft(result, n=2048)
    return torch.fft.ifft(result)


def ihfft_773(device: str) -> torch.Tensor:
    result = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=device)
    result.requires_grad_(True)
    result = torch.fft.ihfft(result)
    result = torch.fft.fft(result, n=2048)
    result = torch.fft.fft(result, n=2048)
    result = torch.fft.fft(result, n=2048)
    result.requires_grad_(True)
    return torch.fft.fft(result, n=2048)


CASES = [
    Case("torch.fft.hfft_570", hfft_570),
    Case("torch.fft.hfft_779", hfft_779),
    Case("torch.fft.hfft_782", hfft_782),
    Case("torch.fft.ifftn_1255", ifftn_1255),
    Case("torch.fft.ihfft_1059", ihfft_1059),
    Case("torch.fft.ihfft_1268", ihfft_1268),
    Case("torch.fft.ihfft_1400", ihfft_1400),
    Case("torch.fft.ihfft_773", ihfft_773),
]


def report_case(case: Case) -> None:
    with torch.no_grad():
        cpu = case.fn("cpu").detach().cpu()
        gpu = case.fn("cuda:0")
        torch.cuda.synchronize()
        gpu = gpu.detach().cpu()

    cpu_finite = torch.isfinite(cpu)
    gpu_finite = torch.isfinite(gpu)
    common = cpu_finite & gpu_finite
    finite_mask_equal = torch.equal(cpu_finite, gpu_finite)

    print(f"case={case.name}")
    print(f"shape={tuple(cpu.shape)} dtype={cpu.dtype}")
    print(f"finite_mask_equal={finite_mask_equal}")
    print(f"cpu_finite={cpu_finite.sum().item()}/{cpu.numel()}")
    print(f"gpu_finite={gpu_finite.sum().item()}/{gpu.numel()}")

    if common.any():
        diff = (cpu[common] - gpu[common]).abs()
        base = torch.maximum(cpu[common].abs(), torch.full_like(diff, 1e-12))
        rel = diff / base
        print(f"max_abs={diff.max().item():.9g}")
        print(f"mean_abs={diff.mean().item():.9g}")
        print(f"max_rel={rel.max().item():.9g}")
        for tol in (1e-5, 1e-4, 1e-3, 1e-2):
            ok = torch.allclose(cpu[common], gpu[common], rtol=tol, atol=tol)
            print(f"allclose_{tol:g}={ok}")
    else:
        print("no_common_finite_values=True")

    print()


def main() -> None:
    print("torch:", torch.__version__)
    print("cuda:", torch.version.cuda)
    if not torch.cuda.is_available():
        raise SystemExit("CUDA is not available")
    print("device:", torch.cuda.get_device_name(0))
    print()

    for case in CASES:
        report_case(case)


if __name__ == "__main__":
    main()
