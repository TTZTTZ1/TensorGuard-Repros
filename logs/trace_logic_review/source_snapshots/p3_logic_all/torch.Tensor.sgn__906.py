
_input_tensor = torch.rand(5, 7).unsqueeze(0)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
