
indices = torch.as_tensor([[0, 0, 1, 1], [0, 1, 0, 1]], dtype=torch.long)
values = torch.tensor([0.5, (- 0.4), 0.6, (- 0.2)], dtype=torch.float32)
size = torch.Size([2, 2])
dim = 0
sparse_tensor = torch.sparse.FloatTensor(indices, values, size)
result = torch.sparse.softmax(sparse_tensor, dim)
result = result.sum(dim=1)
result = torch.sparse.sum(result, dim)
