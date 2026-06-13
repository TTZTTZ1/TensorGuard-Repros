import torch

print("torch:", torch.__version__)

row_indices = torch.arange(4).long()
col_indices = torch.tensor([0, 2, 1, 3])
values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32)

sparse_tensor = torch.sparse_csr_tensor(
    row_indices,
    col_indices,
    values,
    torch.Size([2, 2]),
)

print("before torch.mm sparse_tensor, sparse_tensor", flush=True)
result = torch.mm(sparse_tensor, sparse_tensor)
print(result)

print("before torch.mm sparse_tensor, sparse_tensor.t()", flush=True)
result = torch.mm(sparse_tensor, sparse_tensor.t())
print(result)
