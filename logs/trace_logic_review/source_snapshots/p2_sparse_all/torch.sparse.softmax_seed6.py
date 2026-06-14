indices = torch.tensor([[0, 1], [2, 0]])
values = torch.tensor([1.0, 2.0])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(2, 3), requires_grad=True)
dim = 1
output = torch.sparse.softmax(sparse_tensor, dim)