
mat1 = torch.tensor([[1.0, 2.0], [3.0, 0.0]])
mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
torch.Tensor.addmm_(mat1.t(), mat2, torch.transpose(mat1, 0, 1))
