
_input_tensor = torch.tensor(np.random.random_sample((3,)))
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
