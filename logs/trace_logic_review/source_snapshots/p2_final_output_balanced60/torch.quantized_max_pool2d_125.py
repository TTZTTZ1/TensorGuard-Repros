
input_tensor = torch.FloatTensor(np.random.randint(low=0, high=256, size=[1, 3, 224, 224]))
scale = 0.1
zero_point = 0
quantized_input = torch.quantize_per_tensor(input_tensor, scale, zero_point, torch.qint8)
kernel_size = 2
stride = 2
padding = 0
dilation = 1
ceil_mode = False
output = torch.quantized_max_pool2d(quantized_input, kernel_size, stride, padding, dilation, ceil_mode)
torch.save(output, './quantized_output.pt')
