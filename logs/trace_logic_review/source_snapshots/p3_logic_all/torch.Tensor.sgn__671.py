
_input_tensor = torch.randn(3, 10).requires_grad_()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor).clamp_(0, 1)
