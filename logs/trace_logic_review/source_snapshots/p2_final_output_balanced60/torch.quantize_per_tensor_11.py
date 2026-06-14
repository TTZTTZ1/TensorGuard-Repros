
input_data = torch.tensor([0.5, (- 0.5), 0.0], dtype=torch.float32)
scale = 0.1
zero_point = 0
dtype = torch.qint8
quantized_data = torch.quantize_per_tensor(input_data, scale=scale, zero_point=zero_point, dtype=dtype)
