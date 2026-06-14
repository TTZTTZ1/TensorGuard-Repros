indices = torch.tensor([[0, 1], [2, 0]])
values = torch.tensor([0.2, 0.3])
size = (2, 3)
sparse_input = torch.sparse_coo_tensor(indices, values, size, requires_grad=True)
dim = 1
output = torch.sparse.log_softmax(sparse_input, dim)