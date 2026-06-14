
_input_tensor = torch.tensor(np.random.rand(3, 4)).view((- 1), 3)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
