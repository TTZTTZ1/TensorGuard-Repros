indices = torch.tensor([[0, 0], [1, 1]])
values = torch.tensor([0.5, 0.7])
sparse_input = torch.sparse_coo_tensor(indices, values, (2, 2), requires_grad=True)
dim = 1
output = torch.sparse.log_softmax(sparse_input, dim)