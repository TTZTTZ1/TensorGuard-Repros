
device = torch.device('cpu')
_input_tensor = torch.arange(10, dtype=torch.float32).to(device)
_input_tensor = _input_tensor.cpu()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
