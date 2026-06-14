
input = torch.randn(2, 2, 16)
input = torch.Tensor(input)
indices = torch.argmax(input, dim=2, keepdim=True).expand((- 1), (- 1), input.size(2))
kernel_size = 3
stride = None
padding = 0
output_size = None
result = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding, output_size)
result = result.view(result.size(0), (- 1))
