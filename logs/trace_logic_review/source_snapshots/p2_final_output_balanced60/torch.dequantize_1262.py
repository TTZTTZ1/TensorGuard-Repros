
tensor = torch.quantize_per_tensor(torch.tensor([1.0, 2.0, 3.0]), scale=0.5, zero_point=0, dtype=torch.qint8)
dequantized_tensor = torch.dequantize(tensor)
(dequantized_tensor.min(), (dequantized_tensor.max() == 1.0), dequantized_tensor.eq(torch.tensor([0.0, 2.0, 1.0])))
