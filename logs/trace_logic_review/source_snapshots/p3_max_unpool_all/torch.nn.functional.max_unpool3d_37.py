
input_tensor = torch.randn(1, 16, 4, 4, 4)
indices = torch.argmax(input_tensor, dim=1, keepdim=True).expand_as(input_tensor)
kernel_size = (2, 2, 2)
stride = kernel_size
padding = 0
output_size = None
result = torch.nn.functional.max_unpool3d(input_tensor, indices, kernel_size, stride, padding, output_size)
