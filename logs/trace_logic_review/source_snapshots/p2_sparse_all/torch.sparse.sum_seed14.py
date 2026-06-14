indices = torch.tensor([[0, 1], [2, 0]])
values = torch.tensor([3.0, 4.0])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(2, 3))
result = torch.sparse.sum(sparse_tensor, dim=0)