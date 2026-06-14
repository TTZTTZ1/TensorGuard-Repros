
input_tensor = torch.randn(2, 3)
output_tensor = torch.Tensor.floor_divide_(torch.Tensor.div(input_tensor, 0.1), input_tensor)
