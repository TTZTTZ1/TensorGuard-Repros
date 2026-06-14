
input_data = torch.randn(2, 3)
input_data = input_data.repeat(6, 2)
result = torch.qr(input_data)[0]
