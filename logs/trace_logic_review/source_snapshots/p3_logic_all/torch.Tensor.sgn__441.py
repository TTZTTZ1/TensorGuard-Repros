
_input_tensor = torch.randn((1, 3, 224, 224))
_input_tensor = _input_tensor.view(1, 3, (- 1)).type('torch.FloatTensor')
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
