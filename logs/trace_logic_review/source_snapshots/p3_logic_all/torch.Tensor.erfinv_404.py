
input_tensor = (2.0 * torch.randn(3, 5, 7, 2))
result = torch.Tensor.erf(input_tensor)
output_value = torch.Tensor.erfinv(result)
