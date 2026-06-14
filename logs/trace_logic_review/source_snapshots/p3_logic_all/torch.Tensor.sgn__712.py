
input_tensor = torch.rand((5, 10))
device = 'cpu'
_input_tensor = input_tensor.view(1, (- 1)).to(device)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor).to(device)
