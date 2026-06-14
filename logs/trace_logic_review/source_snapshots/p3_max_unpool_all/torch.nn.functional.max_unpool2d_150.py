
input = torch.randn(5, 5, 8, 8)
input = torch.cat((input, input, input), dim=3)
input = torch.squeeze(input, dim=1)
indices = torch.argmax(input, dim=1, keepdim=True).expand_as(input)
kernel_size = 2
stride = (kernel_size // 2)
result = torch.nn.functional.max_unpool2d(input, indices, kernel_size, stride)
