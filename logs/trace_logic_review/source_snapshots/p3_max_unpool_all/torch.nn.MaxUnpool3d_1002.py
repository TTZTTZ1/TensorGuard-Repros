
input_tensor = torch.randn(1, 1, 4, 4, 4)
indices = torch.argmax(input_tensor, dim=1, keepdim=True)
max_unpool = torch.nn.MaxUnpool3d(2, 2, 2)(input_tensor, indices)
output = max_unpool
output = max_unpool.transpose(1, 2)
max_unpool = torch.squeeze(output)
output_softmax = torch.softmax(max_unpool, dim=1)
max_unpool = torch.squeeze(max_unpool)
output_softmax_argmax = torch.argmax(output_softmax, dim=1, keepdim=True)
unpool = max_unpool
unpool = unpool.transpose(1, 2)
output = max_unpool.transpose(1, 2)
