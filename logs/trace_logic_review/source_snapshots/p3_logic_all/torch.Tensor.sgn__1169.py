
_input_tensor = torch.randn(4, 2).to(torch.device('cpu'))
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
