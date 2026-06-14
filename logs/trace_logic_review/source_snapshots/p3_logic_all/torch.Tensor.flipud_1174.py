
_input_tensor = torch.randn(6, 1, 10, 10, requires_grad=True)
result = torch.Tensor.flipud(torch.argsort(_input_tensor, dim=0))
input_tensor = _input_tensor.detach()
result = torch.flip(result, dims=(0, 1))
input_tensor = torch.cat([_input_tensor, torch.zeros_like(result, dtype=torch.int64)])
result = torch.flip(torch.argsort(input_tensor, dim=0), dims=(0, 1))
