
_input_tensor = torch.tensor(np.random.randn(3, 2)).to('cpu')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
