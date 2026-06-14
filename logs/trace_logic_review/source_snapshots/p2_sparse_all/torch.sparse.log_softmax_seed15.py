indices = torch.tensor([[0, 1], [2, 3]])
values = torch.tensor([0.5, 0.4])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(4, 2))
result = torch.sparse.log_softmax(sparse_tensor, dim=1)