import sys
import torch

device = sys.argv[1]
print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)
print("device:", device)

x = torch.randn(4, 3, device=device)
index = torch.tensor([[0, 1, 3], [0, 1, 2], [0, 1, 2], [0, 1, 2]], device=device)
y = torch.Tensor.gather(x, 1, index)

if device.startswith("cuda"):
    torch.cuda.synchronize()

print(y)
