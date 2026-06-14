input = torch.sparse_coo_tensor([[0, 1, 1], [2, 0, 2]], [3.0, 4.0, 5.0], size=(2, 3))
dim = 1
result = torch.sparse.softmax(input, dim)