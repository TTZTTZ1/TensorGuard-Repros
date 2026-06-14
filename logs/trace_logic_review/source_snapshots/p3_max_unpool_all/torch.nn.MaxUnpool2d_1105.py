
input_tensor = torch.randn(1, 1, 6, 6)
indices = torch.argmax(input_tensor, dim=1, keepdim=True)
max_unpool = torch.nn.MaxUnpool2d(2, 2)
outputs = max_unpool(input_tensor, indices)
