
n = 10000
_input_tensor = (1.0 * torch.randn(n, 2))
(torch.Tensor.polygamma_(_input_tensor, n) - torch.tensor([0.75]))
