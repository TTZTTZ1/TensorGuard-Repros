indices = torch.tensor([[0, 0], [1, 1]])
values = torch.tensor([0.5, 0.9])
shape = (2, 2)
input_sparse = torch.sparse_coo_tensor(indices, values, shape)
dim = 1
output = torch.sparse.softmax(input_sparse, dim=dim)