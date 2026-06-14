
device = torch.device('cpu')
_input_tensor = torch.randn(1, 3, 32).to(device)
_input_tensor = (_input_tensor / 255.0)
_input_tensor = _input_tensor.cpu()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
