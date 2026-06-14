
_input_tensor = np.array([(- 0.01), 0.01, (- 0.02)])
_input_tensor = torch.from_numpy(_input_tensor).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
