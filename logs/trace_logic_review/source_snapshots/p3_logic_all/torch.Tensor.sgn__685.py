
_input_tensor = torch.randn(1, 3, 64, 64).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor).clamp_(0, 1)
