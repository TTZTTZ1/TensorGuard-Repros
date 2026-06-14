
input = torch.randn(1, 16, 5)
indices = torch.argmax(input, dim=2, keepdim=True).expand((- 1), (- 1), input.size(2))
kernel_size = 3
stride = None
padding = 0
result = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding, output_size=None)
