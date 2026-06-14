
_input_tensor = torch.randn(5, 2).to(torch.device('cpu'))
torch.Tensor.sgn_(_input_tensor)
