
input_tensor = torch.randn(3, 4, 5)
output_tensor = torch.Tensor.argsort(input_tensor, descending=True, dim=1)
output_tensor = torch.Tensor.argsort(output_tensor, descending=True, dim=0)
output_tensor = torch.Tensor.argsort(torch.squeeze(output_tensor), descending=False, dim=0)
output_tensor = output_tensor.sort()[0]
output_tensor = torch.Tensor(output_tensor)
output_tensor.size()
