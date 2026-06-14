
_input_tensor = torch.unsqueeze(torch.randn(100, 1, 16, 16), 0).float()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
