
_input_tensor = torch.from_numpy(np.random.randint((- 3), 3, (32, 32, 3)))
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
