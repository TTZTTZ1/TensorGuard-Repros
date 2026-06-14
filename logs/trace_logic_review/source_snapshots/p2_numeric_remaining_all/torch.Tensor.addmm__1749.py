
input_tensor = torch.rand(2, 2)
_input_tensor = input_tensor
mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2))
mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
torch.Tensor.addmm_(mat1, mat2, mat1.transpose(0, 1))
