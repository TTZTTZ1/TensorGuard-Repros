
_input_tensor = torch.randn([1, 5, 5]).float()
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
