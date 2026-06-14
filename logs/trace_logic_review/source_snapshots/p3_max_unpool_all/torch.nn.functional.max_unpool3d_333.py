
input = np.array([[[[3, 3], [3, 3], [5, 5], [4, 4], [4, 2]], [[4, 4], [4, 3], [5, 3], [3, 3], [3, 2]]]], dtype=np.float32)
input = torch.from_numpy(input).type(torch.float)
input = input.repeat([2, 1, 1, 1])
input = torch.as_tensor(input)
indices = torch.argmax(input, dim=1, keepdim=True).expand_as(input)
kernel_size = 2
stride = kernel_size
padding = 0
output_size = None
result = torch.nn.functional.max_unpool3d(input, indices, kernel_size, stride, padding, output_size)
result = result[0].clamp(min=0)
