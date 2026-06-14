indices = torch.tensor([[0, 0], [1, 1]])
values = torch.tensor([0.2, 0.6])
shape = (2, 3)
input_sparse = torch.sparse_coo_tensor(indices, values, shape)
dim = 1
output = torch.sparse.log_softmax(input_sparse, dim)