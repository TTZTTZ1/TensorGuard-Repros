
input_tensor = torch.randn(3, 4, 5)
output_tensor = torch.Tensor.argsort(input_tensor, dim=1).sort()[1]
output_tensor = output_tensor.sort()[0]
output_tensor = torch.Tensor(output_tensor)
output_tensor.size()
