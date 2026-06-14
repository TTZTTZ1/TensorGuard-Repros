
input = torch.Tensor([[2, 3, 4, 9, 3], [1, 2, 3, 5, 4]])
input = torch.unsqueeze(input, dim=0).unsqueeze(1)
input = torch.as_tensor(input)
indices = torch.argmax(input, dim=1, keepdim=True).expand_as(input)
kernel_size = 2
stride = kernel_size
padding = 0
output_size = None
result = torch.nn.functional.max_unpool3d(input, indices, kernel_size, stride, padding, output_size)
result = result[0].clamp(min=0)
