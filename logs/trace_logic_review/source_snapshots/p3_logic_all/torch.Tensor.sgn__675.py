
_input_tensor = torch.randn(2, 3)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor).clamp_(0, 1)
