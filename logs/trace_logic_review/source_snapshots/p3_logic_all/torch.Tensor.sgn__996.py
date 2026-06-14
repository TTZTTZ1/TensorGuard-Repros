
_input_tensor = np.array([0.0, 0.5, 1.0])
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
