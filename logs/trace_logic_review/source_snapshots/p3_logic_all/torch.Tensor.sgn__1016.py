
_input_tensor = torch.rand(3, 2).reshape((3, 2))
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
