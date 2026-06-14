indices = torch.tensor([[0, 0, 1, 1], [0, 2, 0, 2]])
values = torch.tensor([0.5, 0.4, 0.1, 0.8])
sparse_input = torch.sparse_coo_tensor(indices, values, size=(2, 3), requires_grad=True)
dim = 1
output = torch.sparse.log_softmax(sparse_input, dim)