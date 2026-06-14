indices = torch.tensor([[0, 1], [2, 0]])
values = torch.tensor([0.2, 0.3])
size = torch.Size([2, 3])
input_sparse = torch.sparse_coo_tensor(indices, values, size, requires_grad=True)
dim = 1
output = torch.sparse.log_softmax(input_sparse, dim)