
_input_tensor = torch.randn(3, 4).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
_input_tensor = _input_tensor.cpu()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
