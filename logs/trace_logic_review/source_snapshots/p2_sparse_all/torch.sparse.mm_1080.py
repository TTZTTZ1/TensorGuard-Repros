
mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3))
mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 2], [2, 1]]), values=torch.tensor([5.0, 8.0]), size=(3, 3))
_result = torch.sparse.mm(mat1, mat2)
