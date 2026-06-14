
indices = torch.tensor([[0, 1], [1, 0]])
values = torch.tensor([0.6, 0.2])
size = torch.Size([2, 2])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size)
dim = 0
result = torch.sparse.softmax(sparse_tensor, dim)
result = torch.div(result, torch.sum(sparse_tensor))
