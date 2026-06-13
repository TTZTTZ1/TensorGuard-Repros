import torch

print("torch:", torch.__version__)

n = torch.any(torch.not_equal(torch.eye(2).bool(), 1.0))
print("n:", n, "dtype:", n.dtype, "shape:", n.shape)

result = torch.eye(n)
print(result)
