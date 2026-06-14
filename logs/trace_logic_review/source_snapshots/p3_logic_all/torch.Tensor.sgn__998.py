
_input_tensor = (np.random.uniform((- 5), 5, [50, 20]).astype(np.float32) / 50)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
