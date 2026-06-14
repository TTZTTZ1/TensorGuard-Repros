
mat = torch.randn(3, 3, requires_grad=True)
mat1 = torch.sparse_coo_tensor(torch.tensor([[0, 1], [1, 0]]), torch.tensor([1.0, 2.0]), size=(3, 3))
mat2 = torch.randn(3, 3)
result = torch.sparse.addmm(mat2, mat1, mat)
