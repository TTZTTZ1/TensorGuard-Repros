
mat1 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 1], [1, 2]]), values=torch.tensor([1.0, 2.0]), size=(2, 3))
mat2 = torch.sparse_coo_tensor(indices=torch.tensor([[0, 2], [1, 0]]), values=torch.tensor([3.0, 4.0]), size=(3, 2))
_result = torch.sparse.mm(mat1, mat2)
