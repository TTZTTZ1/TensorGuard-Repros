import torch

print("torch:", torch.__version__)

mat1 = torch.sparse_coo_tensor(
    indices=torch.tensor([[0, 1], [1, 2]]),
    values=torch.tensor([1.0, 2.0]),
    size=(2, 3),
)

mat2 = torch.sparse_coo_tensor(
    indices=torch.tensor([[0, 2], [2, 3]]),
    values=torch.tensor([1.0, 3.0]),
    size=(3, 2),
)

print("before sparse.mm", flush=True)
result = torch.sparse.mm(mat1, mat2)
print(result)
