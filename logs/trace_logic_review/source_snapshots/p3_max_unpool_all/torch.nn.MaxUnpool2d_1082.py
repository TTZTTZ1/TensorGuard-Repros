
input_tensor = torch.randn(1, 1, 6, 6)
indices = torch.argmax(input_tensor, dim=1, keepdim=True)
max_unpool = torch.nn.MaxUnpool2d(2, 2)
output = torch.nn.functional.unfold(max_unpool(input_tensor, indices), 2, 2)
output = max_unpool(input_tensor, indices)
output = torch.nn.functional.unfold(output, 2, 2)
max_unpool
