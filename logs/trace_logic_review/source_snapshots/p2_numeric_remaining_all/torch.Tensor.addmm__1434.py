
mat1 = torch.tensor([[1.0, 2.0], [3.4, 5.0]])
mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
torch.Tensor.addmm_(mat1, mat1, mat2.t())
