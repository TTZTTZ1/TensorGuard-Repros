
_input_tensor = torch.randn(5, 3)
_input_tensor = _input_tensor.to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
