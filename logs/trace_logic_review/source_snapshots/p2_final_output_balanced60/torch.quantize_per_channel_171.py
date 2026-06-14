
input_tensor = torch.randn(4, 4, dtype=torch.float32)
scales = torch.tensor(([0.1] * 4), dtype=torch.float32)
zero_points = torch.tensor(([0] * 4), dtype=torch.int32)
axis = 1
dtype = torch.qint8
quantized_tensor = torch.quantize_per_channel(input_tensor, scales, zero_points, axis, dtype)
result = quantized_tensor.clone().detach().cpu()
