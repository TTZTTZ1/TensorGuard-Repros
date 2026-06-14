input = torch.randn(1, 1, 6)
indices = torch.tensor([[[1, 1, 1, 1, 1, 1]]])
kernel_size = 2
stride = None
padding = 0
output_size = None
output = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding, output_size)