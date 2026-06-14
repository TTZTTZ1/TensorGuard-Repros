input = torch.sparse_coo_tensor([[0, 1], [1, 0]], [1.0, 2.0], (2, 2))
dim = 1
result = torch.sparse.log_softmax(input, dim)