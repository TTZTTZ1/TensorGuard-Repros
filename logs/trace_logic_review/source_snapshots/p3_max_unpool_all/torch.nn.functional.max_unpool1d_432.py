
input = torch.randn(1, 20, 20)
input = torch.Tensor(input)
indices = torch.argmax(input, dim=2, keepdim=True).expand((- 1), (- 1), input.size(2))
kernel_size = 3
stride = None
padding = 0
output_size = None
result = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding, output_size=output_size)
result
