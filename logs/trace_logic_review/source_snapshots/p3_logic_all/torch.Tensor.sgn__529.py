
_input_tensor = torch.Tensor([[[1, 2, 3, 4, 5, 6, 7, 8]]])
_input_tensor = _input_tensor.cpu()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
