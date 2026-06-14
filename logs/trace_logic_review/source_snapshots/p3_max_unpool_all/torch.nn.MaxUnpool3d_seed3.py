input_tensor = torch.randn(1, 16, 32, 32, 32)
indices = torch.randint(0, 2, (1, 16, 32, 32, 32))
max_unpool3d = torch.nn.MaxUnpool3d(kernel_size=2, stride=2, padding=0)
output_tensor = max_unpool3d(input_tensor, indices)