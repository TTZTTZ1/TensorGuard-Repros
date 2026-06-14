indices = torch.tensor([[0, 0], [1, 1]])
values = torch.tensor([0.5, 0.8])
sparse_input = torch.sparse_coo_tensor(indices, values, size=(2, 2), requires_grad=True)
dim = 1
result = torch.sparse.log_softmax(sparse_input, dim)