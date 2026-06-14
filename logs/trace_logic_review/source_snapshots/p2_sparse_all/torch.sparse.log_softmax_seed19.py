indices = torch.tensor([[0, 1], [2, 0]])
values = torch.tensor([1.0, 2.0])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(3, 2))
output = torch.sparse.log_softmax(sparse_tensor, dim=1)