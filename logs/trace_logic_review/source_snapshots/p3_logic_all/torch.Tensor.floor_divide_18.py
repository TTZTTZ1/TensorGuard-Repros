
input_tensor = torch.randn(3, 3)
output_tensor = torch.Tensor.floor_divide(torch.Tensor.div(input_tensor, 0.1), input_tensor)
