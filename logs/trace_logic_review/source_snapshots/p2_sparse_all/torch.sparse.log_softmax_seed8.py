indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([0.5, 0.3, 0.2])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(2, 3))
result = torch.sparse.log_softmax(sparse_tensor, dim=1)