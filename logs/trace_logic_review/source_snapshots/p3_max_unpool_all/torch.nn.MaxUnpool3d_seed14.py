input_tensor = torch.randn(1, 16, 8, 8, 8)
indices = torch.randint(0, 16, (1, 16, 8, 8, 8))
max_unpool3d = torch.nn.MaxUnpool3d(kernel_size=2, stride=2, padding=0)
output = max_unpool3d(input_tensor, indices)