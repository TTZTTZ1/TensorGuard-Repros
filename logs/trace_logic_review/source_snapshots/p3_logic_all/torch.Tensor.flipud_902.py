
_input_tensor = torch.randn(6, 1, 10, 10, requires_grad=True)
result = torch.Tensor.flipud(torch.argsort(_input_tensor, dim=0))
input_tensor = torch.cat([_input_tensor, torch.zeros_like(result)])
result = torch.Tensor.flipud(torch.argsort(input_tensor, dim=0))
