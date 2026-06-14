
scales = torch.tensor([0.5, 0.75, 1.0, 1.25])
zero_points = torch.tensor([0, 0, 0, 0], dtype=torch.int32)
axis = 1
dtype = torch.qint8
quantized_tensor = torch.quantize_per_channel(torch.rand(4, 4, dtype=torch.float32), scales, zero_points, axis, dtype)
