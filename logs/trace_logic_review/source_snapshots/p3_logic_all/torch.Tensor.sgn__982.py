
_input_tensor = np.array([0, 3, (- 1)], dtype=np.float32)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
