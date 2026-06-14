input = torch.randn(1, 16, 50)
indices = torch.argmax(input, dim=(- 1), keepdim=True).expand((- 1), (- 1), input.size((- 1)))
kernel_size = 3
stride = 2
padding = 1
output = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding)