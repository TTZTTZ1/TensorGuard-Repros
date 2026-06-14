
tensor = torch.randn(3, 4, 5)
output_tensor = torch.Tensor.argsort(tensor, dim=1, descending=True)[0]
output_tensor = output_tensor.argsort(dim=1, descending=False)[0]
output_tensor = torch.Tensor(output_tensor)
output_tensor.size()
output_tensor = torch.Tensor(output_tensor)
output_tensor = output_tensor.sort()[0]
output_tensor = torch.Tensor(output_tensor)
output_tensor.size()
