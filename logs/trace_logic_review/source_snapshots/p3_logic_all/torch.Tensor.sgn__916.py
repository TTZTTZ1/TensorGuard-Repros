
_input_tensor = torch.rand((1, 2, 3), requires_grad=True)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
