
input_data = torch.randn(3, 16)
result = torch.qr(torch.mm(torch.tensor(input_data).t(), input_data))[0]
