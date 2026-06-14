
input = torch.randn(1, 16, 50, 50)
indices = torch.argmax(input, dim=1, keepdim=True).expand_as(input)
kernel_size = 2
stride = kernel_size
padding = 0
output_size = None
result = torch.nn.functional.max_unpool2d(input, indices, kernel_size, stride, padding, output_size)
