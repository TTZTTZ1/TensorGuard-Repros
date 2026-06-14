
_input_tensor = torch.LongTensor([[1, 2], [0, 1], [2, 3], [4, 5], [5, 1]])
result = torch.Tensor.flipud(torch.argsort(_input_tensor, dim=0))
result = result.unsqueeze(0)
result = result.permute(1, 0, 2)
