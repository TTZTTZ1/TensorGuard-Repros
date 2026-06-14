
mat1 = torch.tensor([[10.0, 11.0], [12.0, 13.0]])
mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
torch.Tensor.addmm_(mat1, mat2, mat1.t())
