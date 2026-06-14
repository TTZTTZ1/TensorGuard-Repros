
input = torch.randn(1, 20, 20)
input = torch.Tensor(input)
indices = torch.argmax(input, dim=2, keepdim=True).expand((- 1), (- 1), input.size(2))
kernel_size = 3
stride = None
result = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride)
result = torch.sum(result, dim=2)
result = torch.abs(result)
result = torch.round(result)
result = torch.sigmoid(result)
result = torch.sum(result, dim=1)
