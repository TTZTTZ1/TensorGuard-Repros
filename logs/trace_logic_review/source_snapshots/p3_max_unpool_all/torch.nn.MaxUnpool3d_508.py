
input_tensor = torch.randn(1, 1, 4, 4, 4)
indices = torch.argmax(input_tensor, dim=1, keepdim=True)
max_unpool = torch.nn.MaxUnpool3d(kernel_size=4, stride=4)(input_tensor, indices)
max_unpool = torch.squeeze(max_unpool)
