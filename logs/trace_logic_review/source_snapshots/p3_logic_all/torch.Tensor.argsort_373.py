
input_tensor = torch.randn(3, 4, 5)
output_tensor = torch.Tensor.argsort(torch.argsort(input_tensor, dim=0)[0][0], dim=0)
