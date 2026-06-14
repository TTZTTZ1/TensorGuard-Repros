input_tensor = torch.randn(1, 1, 4, 4, 4)
indices = torch.argmax(input_tensor, dim=2, keepdim=True).expand((- 1), (- 1), 4, 4, 4)
max_unpool = torch.nn.MaxUnpool3d(kernel_size=2, stride=2, padding=0)
output = max_unpool(input_tensor, indices)