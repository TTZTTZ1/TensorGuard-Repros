
_input_tensor = torch.randint(low=0, high=(2 ** 30), size=(1, 3))
_input_tensor = _input_tensor.cpu()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
