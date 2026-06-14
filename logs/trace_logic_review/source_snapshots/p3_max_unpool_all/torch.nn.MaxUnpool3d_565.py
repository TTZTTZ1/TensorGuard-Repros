
input_tensor = torch.randn(3, 32, 32)
input_tensor = input_tensor[(None, None, ...)]
indices = torch.argmax(input_tensor, dim=1, keepdim=True)
max_unpool = torch.nn.MaxUnpool3d(2, 2, 2)(input_tensor, indices)
max_unpool = torch.squeeze(max_unpool)
max_unpool.shape
