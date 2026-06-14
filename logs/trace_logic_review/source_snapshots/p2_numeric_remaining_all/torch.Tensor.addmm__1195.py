
_input_tensor = torch.zeros(2, 2)
_input_tensor = (_input_tensor + (torch.randn_like(_input_tensor).unsqueeze(dim=0) * 3))
mat1 = torch.FloatTensor(_input_tensor.reshape(2, 2))
mat2 = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
torch.Tensor.addmm_(mat2, mat1, mat2.t())
