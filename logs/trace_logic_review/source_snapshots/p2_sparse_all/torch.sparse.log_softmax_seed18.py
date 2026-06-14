indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([1.0, 2.0, 3.0])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(3, 4), requires_grad=True)
dim = 1
output = torch.sparse.log_softmax(sparse_tensor, dim)