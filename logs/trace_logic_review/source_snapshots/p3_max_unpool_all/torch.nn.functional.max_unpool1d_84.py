
input = np.array([[1, 2, 3, 4], [1, 3, 2, 1], [3, 2, 3, 1]])
input = np.reshape(input, (1, 3, 4))
input = torch.Tensor(input)
indices = torch.argmax(input, dim=2, keepdim=True).expand((- 1), (- 1), input.size(2))
kernel_size = 3
stride = None
padding = 0
output_size = None
result = torch.nn.functional.max_unpool1d(input, indices, kernel_size, stride, padding, output_size)
result
