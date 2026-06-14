
_input_tensor = (torch.tensor([1, 2, 3]) / 10)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
