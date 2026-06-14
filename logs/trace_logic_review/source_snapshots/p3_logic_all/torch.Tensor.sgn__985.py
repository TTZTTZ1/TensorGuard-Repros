
_input_tensor = torch.LongTensor([[1, 2, 3]])
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
