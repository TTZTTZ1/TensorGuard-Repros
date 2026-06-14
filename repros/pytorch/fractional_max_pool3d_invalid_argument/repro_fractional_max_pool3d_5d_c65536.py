import sys
import torch
import torch.nn.functional as F

device = sys.argv[1] if len(sys.argv) > 1 else "cpu"

print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("device:", device)

torch.manual_seed(420)

x = torch.randn(1, 65536, 4, 4, 4, device=device)

print("x.shape:", tuple(x.shape))

y = F.fractional_max_pool3d(
    x,
    kernel_size=(2, 2, 2),
    output_size=(1, 1, 1),
)

if device.startswith("cuda"):
    torch.cuda.synchronize()

print("ok")
print("y.shape:", tuple(y.shape))
