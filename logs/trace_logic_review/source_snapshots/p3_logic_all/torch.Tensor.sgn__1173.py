
_input_tensor = torch.randn(5, 2).to(torch.device('cpu'))
_input_tensor = _input_tensor.repeat(1, 2, 1)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
