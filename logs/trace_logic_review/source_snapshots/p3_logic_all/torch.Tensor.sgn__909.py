
_input_tensor = torch.randn(3, 8, 8, 8).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
