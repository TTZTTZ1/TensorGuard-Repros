mat = torch.randn(5, 5)
mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [2, 3]]), values=torch.tensor([1.0, 2.0]), size=(5, 5))
mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [2, 3]]), values=torch.tensor([3.0, 4.0]), size=(5, 5))
result = torch.sparse.addmm(mat, mat1, mat2.to_dense())