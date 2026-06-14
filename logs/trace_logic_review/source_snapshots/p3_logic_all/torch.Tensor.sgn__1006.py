
input_size = 64
_input_tensor = ((2 * torch.randn(input_size, dtype=torch.float32)) - 1)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
