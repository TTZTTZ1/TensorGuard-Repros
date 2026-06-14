
input = torch.randn(1, 20, 20)
input = torch.Tensor(input)
indices = torch.argmax(input, dim=2, keepdim=True).expand((- 1), (- 1), input.size(2))
kernel_size = 3
stride = None
padding = 0
result = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding, output_size=None)
result = result.reshape((- 1), result.size(2))
result = ((result - result.min()) / (result.max() - result.min()))
result = result.unsqueeze(0).unsqueeze((- 1)).unsqueeze((- 1))
result = torch.tanh(result)
result = torch.round((result * 5))
result = torch.floor(((result - result) + 1))
result = torch.sum(result, dim=1)
result = torch.abs(result)
result = result.squeeze(0)
