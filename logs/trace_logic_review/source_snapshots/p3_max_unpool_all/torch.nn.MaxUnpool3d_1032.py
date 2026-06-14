
input_tensor = torch.randn(1, 1, 4, 4, 4)
indices = torch.argmax(input_tensor, dim=1, keepdim=True)
max_unpool = torch.nn.MaxUnpool3d(2, 2, 2)(input_tensor, indices)
output = max_unpool
output = max_unpool.transpose(1, 2)
max_unpool = torch.squeeze(output)
output = output.unsqueeze(2).unsqueeze(2).unsqueeze(3)
max_unpool = torch.squeeze(output)
output = max_unpool.transpose(1, 2)
