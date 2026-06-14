
input_tensor = torch.randn(1, 1, 4, 4, 4)
indices = torch.argmax(input_tensor, dim=1, keepdim=True)
max_unpool = torch.nn.MaxUnpool3d(2, 2, 2)(input_tensor, indices)
output_unpool = torch.nn.Upsample(scale_factor=4, mode='nearest')(max_unpool)
output = max_unpool.transpose(2, 3)
output_list = [output]
output_list += [output_unpool]
