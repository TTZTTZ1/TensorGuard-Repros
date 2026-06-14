
device = 'cpu'
_input_tensor = torch.tensor(np.array([0, 0.5, 1])).unsqueeze(0)
_input_tensor = _input_tensor.to('cpu')
torch.Tensor.sgn_(_input_tensor).to(device)
