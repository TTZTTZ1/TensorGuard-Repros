
_input_tensor = torch.randn(6, 1, 10, 10, requires_grad=True)
result = torch.Tensor.flipud(torch.argsort(_input_tensor, dim=0))
input_tensor = _input_tensor.detach()
result = torch.flip(result, dims=(0, 1))
input_tensor = torch.cat([_input_tensor, torch.zeros_like(result, dtype=torch.int64)])
result = torch.flip(result, dims=(1,))
input_tensor = torch.cat([input_tensor, torch.zeros_like(input_tensor)], 0)
input_tensor = input_tensor[torch.randperm(input_tensor.size()[0])]
input_tensor = torch.unsqueeze(input_tensor, dim=0)
(result, _) = torch.sort(input_tensor, dim=1, descending=False)
result = torch.flip(result, dims=(0,))
