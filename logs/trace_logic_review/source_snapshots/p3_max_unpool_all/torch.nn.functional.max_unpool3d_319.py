
input = np.random.rand(4, 8, 2, 2)
input = torch.as_tensor(input)
input = torch.as_tensor(input)
indices = torch.argmax(input, dim=1, keepdim=True).expand_as(input)
kernel_size = 2
stride = kernel_size
padding = 0
output_size = None
result = torch.nn.functional.max_unpool3d(input, indices, kernel_size, stride, padding, output_size)
result = result[0].clamp(min=0)
