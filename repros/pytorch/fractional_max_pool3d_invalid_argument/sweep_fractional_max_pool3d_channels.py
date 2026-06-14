import sys
import torch
import torch.nn.functional as F

device = sys.argv[1] if len(sys.argv) > 1 else "cpu"
print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("device:", device)

channel_counts = [
    1, 8, 64, 512, 4096,
    16384, 32768, 65535, 65536, 70000, 76800
]

for c in channel_counts:
    print(f"\n===== C={c} =====", flush=True)
    try:
        x = torch.randn(c, 4, 4, 4, device=device)
        y = F.fractional_max_pool3d(
            x,
            kernel_size=(2, 2, 2),
            output_size=(1, 1, 1),
        )
        if device.startswith("cuda"):
            torch.cuda.synchronize()
        print("OK", tuple(y.shape), flush=True)
    except Exception as e:
        print(type(e).__name__ + ":", e, flush=True)
