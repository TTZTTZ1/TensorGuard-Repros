input = torch.sparse_coo_tensor([[0, 1, 1], [2, 0, 2]], [3, 4, 5], size=(2, 3))
result = torch.sparse.sum(input, dim=1)