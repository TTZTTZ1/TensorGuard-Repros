
input = torch.Tensor(1, 7, 7)
input = torch.Tensor(input)
indices = torch.argmax(input, dim=2, keepdim=True).expand((- 1), (- 1), input.size(2))
kernel_size = 3
stride = None
padding = 0
output_size = None
result = torch.nn.functional.max_unpool1d(input, indices=indices, kernel_size=kernel_size, stride=stride, padding=padding, output_size=output_size)
