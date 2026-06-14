
_input_tensor = torch.rand((10, 3, 5)).type(torch.FloatTensor).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
