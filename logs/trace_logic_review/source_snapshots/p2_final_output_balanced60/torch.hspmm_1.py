
mat1 = torch.sparse_coo_tensor(torch.tensor([[0, 1], [2, 3]]), torch.tensor([1.0, 2.0]), (4, 5))
mat2 = torch.randn(5, 8)
result = torch.hspmm(mat1, mat2)
