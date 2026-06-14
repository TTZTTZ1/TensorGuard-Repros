
device = torch.device('cpu')
_input_tensor = torch.randn(1, 28, 28).to(device)
_input_tensor = _input_tensor.cpu()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
