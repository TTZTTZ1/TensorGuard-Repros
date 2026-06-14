indices = torch.tensor([[0, 1], [2, 0]], dtype=torch.long)
values = torch.tensor([0.5, 0.3], dtype=torch.float)
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(3, 3))
result = torch.sparse.log_softmax(sparse_tensor, dim=1)