indices = torch.tensor([[0, 0], [1, 1]])
values = torch.tensor([1.0, 2.0])
size = torch.Size([2, 3])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size, requires_grad=True)
dim = 0
result = torch.sparse.softmax(sparse_tensor, dim)