
_input_tensor = torch.tensor(np.random.rand(4, 2))
_input_tensor = _input_tensor.cpu()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
