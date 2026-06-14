
input_tensor = torch.randn(3, 3)
output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, descending=True, dim=0))
