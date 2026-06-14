
_input_tensor = torch.randint(low=0, high=8, size=(4, 5)).float()
result = torch.Tensor.flipud(torch.argsort(_input_tensor, dim=0))
result = result.unsqueeze(0)
result = result.permute(1, 0, 2)
