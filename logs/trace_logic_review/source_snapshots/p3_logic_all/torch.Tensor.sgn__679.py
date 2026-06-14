
_input_tensor = [1, 2, 3, 4, 5, 6, 7, 8, 9]
_input_tensor = np.array(_input_tensor)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor).clamp_(0, 1)
