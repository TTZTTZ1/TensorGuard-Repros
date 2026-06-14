
_input_tensor = (2 * torch.rand(4, 2).to('cpu').requires_grad_(requires_grad=True))
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
