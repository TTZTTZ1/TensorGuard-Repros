import sys
import torch

device = sys.argv[1]
print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("device:", device)

x = torch.tensor([1, 2], dtype=torch.int32, device=device)
indices = torch.arange(3, device=device)
y = torch.Tensor.take(x, indices)

if device.startswith("cuda"):
    torch.cuda.synchronize()

print(y)
