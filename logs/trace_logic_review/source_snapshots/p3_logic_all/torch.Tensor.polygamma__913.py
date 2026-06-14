
n = 3000
_input_tensor = torch.randn(2, 3, n)
(torch.Tensor.polygamma_(_input_tensor, n) - torch.tensor([0.75]))
