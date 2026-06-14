mat = torch.randn(4, 4)
mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [2, 3]]), values=torch.tensor([1.0, 2.0]), size=(4, 4))
mat2 = torch.randn(4, 4)
result = torch.sparse.addmm(mat, mat1, mat2)