input = torch.randn(1, 16, 15)
indices = torch.argmax(input, dim=(- 1), keepdim=True).expand_as(input)
kernel_size = 3
stride = 2
padding = 1
output = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding)