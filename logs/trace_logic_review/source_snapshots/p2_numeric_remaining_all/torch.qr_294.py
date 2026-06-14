
input_data = torch.randn(3, 6)
result = torch.qr(torch.mm(input_data.t(), input_data))[0]
