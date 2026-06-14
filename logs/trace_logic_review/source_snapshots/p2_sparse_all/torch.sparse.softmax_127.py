
indices = torch.tensor([[0, 0, 1, 1], [0, 1, 0, 1]], dtype=torch.long)
values = torch.tensor([0.5, (- 0.4), 0.6, (- 0.2)], dtype=torch.float32)
size = torch.Size([2, 2])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size)
dim = 0
result = torch.sparse.softmax(sparse_tensor, dim, dtype=torch.float32)
result = result.to_dense()
result = result.cpu()
