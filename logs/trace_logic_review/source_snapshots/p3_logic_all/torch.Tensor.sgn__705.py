
_input_tensor = (2 * torch.rand(1).type(torch.FloatTensor))
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor).clamp_(0, 1)
