
_input_tensor = np.random.uniform((- 1), 1, [16, 4, 1])
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
