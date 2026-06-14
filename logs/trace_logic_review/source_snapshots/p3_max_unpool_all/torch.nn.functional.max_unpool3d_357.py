
input = torch.rand((4, 3, 224, 224), requires_grad=True)
input = torch.as_tensor(input)
input = torch.transpose(input, 2, 3)
input = torch.tensor(input, dtype=torch.float32)
input = torch.as_tensor(input)
indices = torch.argmax(input, dim=1, keepdim=True).expand_as(input)
kernel_size = 2
stride = kernel_size
padding = 0
result = torch.nn.functional.max_unpool3d(input, indices, kernel_size, stride, padding)
result = result.squeeze(dim=1)
result = result[0].clamp(min=0)
