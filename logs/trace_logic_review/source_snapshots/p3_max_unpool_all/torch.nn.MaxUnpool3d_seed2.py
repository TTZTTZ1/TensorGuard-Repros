input_tensor = torch.randn(1, 16, 4, 4, 4)
indices = torch.randint(0, 2, (1, 16, 4, 4, 4))
max_unpool = torch.nn.MaxUnpool3d(kernel_size=2, stride=2, padding=0)
output_tensor = max_unpool(input_tensor, indices)