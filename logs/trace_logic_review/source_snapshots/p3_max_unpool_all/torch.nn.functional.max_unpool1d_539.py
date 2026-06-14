
input = torch.randn(1, 20, 20)
input = torch.Tensor(input)
indices = torch.argmax(input, dim=2, keepdim=True).expand((- 1), (- 1), input.size(2))
stride = None
result = torch.nn.functional.max_unpool1d(input=input, indices=indices, kernel_size=2, stride=stride)
result = result.view
