
_input_tensor = np.random.randint(0, 1000, 3)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
