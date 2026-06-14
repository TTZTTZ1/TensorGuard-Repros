
_input_tensor = torch.FloatTensor(np.random.randn(5, 10))
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
