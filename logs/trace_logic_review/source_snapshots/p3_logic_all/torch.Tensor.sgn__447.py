
_input_tensor = torch.linspace((- 1), 1, 10).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
