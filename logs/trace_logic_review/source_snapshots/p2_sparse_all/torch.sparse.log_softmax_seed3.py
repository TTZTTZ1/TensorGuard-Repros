indices = torch.tensor([[0, 0], [1, 1]])
values = torch.tensor([0.5, 0.2])
size = torch.Size([2, 2])
input_sparse = torch.sparse_coo_tensor(indices, values, size, requires_grad=True)
dim = 1
output = torch.sparse.log_softmax(input_sparse, dim)