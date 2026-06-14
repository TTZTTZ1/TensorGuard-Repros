
_input_tensor = torch.rand(1, 3, 32, 32).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor).clamp_(0, 1)
