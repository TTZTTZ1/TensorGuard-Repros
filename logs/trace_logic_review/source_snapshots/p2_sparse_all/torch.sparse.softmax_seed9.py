indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([1.0, 2.0, 3.0])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(3, 4))
dim = 1
softmax_output = torch.sparse.softmax(sparse_tensor, dim=dim)