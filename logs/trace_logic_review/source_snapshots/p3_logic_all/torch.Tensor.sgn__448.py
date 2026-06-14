
_input_tensor = torch.randn(1, 3, 128, 128)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
