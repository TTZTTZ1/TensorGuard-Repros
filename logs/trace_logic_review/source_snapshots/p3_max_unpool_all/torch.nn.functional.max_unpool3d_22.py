
input = torch.randn(1, 16, 8, 8, 8)
indices = torch.argmax(input, dim=1, keepdim=True).expand_as(input)
kernel_size = (2, 2, 2)
stride = kernel_size
output_size = None
output = torch.nn.functional.max_unpool3d(input, indices, kernel_size, stride, 0, output_size=output_size)
