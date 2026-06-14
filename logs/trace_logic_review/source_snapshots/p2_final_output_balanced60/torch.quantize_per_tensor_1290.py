
input_data = torch.tensor([(- 0.5), 0.0, 0.5], dtype=torch.float32)
scale = 0.1
zero_point = (- 64)
dtype = torch.qint8
quantized_tensor = torch.quantize_per_tensor(input_data, scale, zero_point, dtype)
torch.save(quantized_tensor, 'input_quantization.pt')
quantized_tensor = quantized_tensor.to(dtype=torch.qint8)
torch.save(quantized_tensor, 'output_quantization.pt')
