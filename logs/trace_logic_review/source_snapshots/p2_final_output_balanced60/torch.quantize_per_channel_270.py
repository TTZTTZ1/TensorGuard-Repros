
input_tensor = torch.randn(4, 4)
scales = torch.tensor([0.5, 1.0, 1.5, 2.0])
zero_points = torch.tensor([0, 1, 2, 3], dtype=torch.long)
axis = 1
dtype = torch.qint8
quantized_tensor = torch.quantize_per_channel(input_tensor, scales, zero_points, axis, dtype)
