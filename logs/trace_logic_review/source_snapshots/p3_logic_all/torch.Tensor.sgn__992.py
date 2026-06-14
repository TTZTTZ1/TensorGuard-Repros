
_input_tensor = torch.randn(1000, 10, 3, 1).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
