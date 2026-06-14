indices = torch.tensor([[0, 1], [2, 0]])
values = torch.tensor([0.2, 0.8])
size = torch.Size([2, 3])
input_sparse = torch.sparse_coo_tensor(indices, values, size)
dim = 1
result = torch.sparse.log_softmax(input_sparse, dim)