input = torch.randn(1, 16, 5)
indices = torch.randint(0, 5, (1, 16, 5))
kernel_size = 2
stride = None
padding = 0
output_size = None
output = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding, output_size)