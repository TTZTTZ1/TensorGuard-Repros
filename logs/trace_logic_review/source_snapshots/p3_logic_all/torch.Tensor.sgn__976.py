
_input_tensor = torch.randn(10, 3, 224, 224)
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
