
_input_tensor = torch.randn([5, 2, 5])
_input_tensor = torch.tensor(_input_tensor).to('cpu')
torch.Tensor.sgn_(_input_tensor)
