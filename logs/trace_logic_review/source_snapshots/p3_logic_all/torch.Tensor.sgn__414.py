
_input_tensor = np.random.randn(10, 3, 64)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
