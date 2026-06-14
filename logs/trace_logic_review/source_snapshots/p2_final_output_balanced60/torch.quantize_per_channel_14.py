
input_tensor = torch.randn(4, 4)
scales = torch.tensor([0.5, 0.75, 1.0, 1.25])
zero_points = torch.tensor([0, 1, 2, 3])
axis = 0
dtype = torch.qint8
quantized_tensor = torch.quantize_per_channel(input_tensor, scales=scales, zero_points=zero_points, axis=axis, dtype=dtype)
