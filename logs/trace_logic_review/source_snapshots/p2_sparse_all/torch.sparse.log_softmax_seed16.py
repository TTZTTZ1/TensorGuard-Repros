indices = torch.tensor([[0, 0, 1, 1], [0, 1, 0, 1]])
values = torch.tensor([0.5, 0.2, 0.8, 0.1])
size = (2, 2)
input_sparse = torch.sparse_coo_tensor(indices, values, size, requires_grad=True)
dim = 1
output = torch.sparse.log_softmax(input_sparse, dim)