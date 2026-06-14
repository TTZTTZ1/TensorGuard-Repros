
_input_tensor = torch.randn(1, 10, 20, 100).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
