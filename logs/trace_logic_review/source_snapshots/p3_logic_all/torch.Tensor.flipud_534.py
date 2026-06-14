
_input_tensor = torch.LongTensor(np.random.randint(0, 5, (5, 4)))
result = torch.Tensor.flipud(torch.argsort(_input_tensor, dim=0))
result = result.unsqueeze(0)
result = result.permute(1, 0, 2)
