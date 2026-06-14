
mat1 = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
torch.Tensor.addmm_(mat1, mat1, mat1.t())
