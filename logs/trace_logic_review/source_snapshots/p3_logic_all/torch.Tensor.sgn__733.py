
device = torch.device('cpu')
_input_tensor = torch.randn(3, 2)
_input_tensor = ((_input_tensor + torch.randn((3, 1))) - 1)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor).to(device)
