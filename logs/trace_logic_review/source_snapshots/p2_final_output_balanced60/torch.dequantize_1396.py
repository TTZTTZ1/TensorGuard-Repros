
tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8)
tensor = tensor.unsqueeze(dim=0)
tensor = torch.as_tensor(tensor)
result = torch.dequantize(tensor)
result
