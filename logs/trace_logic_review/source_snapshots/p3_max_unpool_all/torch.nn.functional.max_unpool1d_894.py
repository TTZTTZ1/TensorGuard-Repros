
input = torch.randn(1, 20, 20)
input = torch.Tensor(input)
indices = torch.argmax(input, dim=2, keepdim=True).expand((- 1), (- 1), input.size(2))
kernel_size = 3
stride = None
padding = 0
result = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding)
result = torch.sum(result, dim=2)
result = torch.abs(result)
result = torch.round(result)
result = torch.clip(result, (- 1), 1)
result = torch.sum(result, dim=1)
