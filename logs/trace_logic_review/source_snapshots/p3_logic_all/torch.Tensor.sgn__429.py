
_input_tensor = np.reshape(np.arange(((3 * 3) * 3)), ((- 1), 3, 3))
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
