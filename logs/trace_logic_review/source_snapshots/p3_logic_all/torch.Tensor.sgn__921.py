
_input_tensor = torch.rand(10, 100).view((- 1), 100)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
