
tensor = torch.quantize_per_tensor(torch.tensor([0.5, 1.5, 2.5]), scale=0.1, zero_point=128, dtype=torch.quint8)
dequantized_tensor = torch.dequantize(tensor)
