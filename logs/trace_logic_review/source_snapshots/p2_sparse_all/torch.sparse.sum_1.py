
indices = torch.tensor([[0, 1], [2, 3]])
values = torch.tensor([1.0, 2.0])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(4, 4))
result = torch.sparse.sum(sparse_tensor, dim=0)
