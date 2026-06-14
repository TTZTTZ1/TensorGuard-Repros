
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
sparse_tensor = torch.sparse.FloatTensor(indices, values, size=(3, 3))
result = torch.sparse.sum(sparse_tensor, dim=1)
