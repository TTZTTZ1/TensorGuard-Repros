
_input_tensor = np.random.rand(2, 3, 3)
_input_tensor = torch.from_numpy(_input_tensor)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
