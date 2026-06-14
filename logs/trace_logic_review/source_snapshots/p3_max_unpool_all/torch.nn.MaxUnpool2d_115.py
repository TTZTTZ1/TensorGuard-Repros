
input_tensor = torch.randn(1, 16, 56, 56)
indices = torch.argmax(input_tensor, dim=1, keepdim=True).expand_as(input_tensor)
indices = indices.sort()[0]
max_unpool = torch.nn.MaxUnpool2d(kernel_size=2, stride=2, padding=0)
output = max_unpool(input_tensor, indices)
