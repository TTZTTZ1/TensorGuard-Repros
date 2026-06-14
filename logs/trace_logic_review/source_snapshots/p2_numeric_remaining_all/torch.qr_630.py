
input_data = torch.arange(3, dtype=torch.float)
input_data = torch.nn.functional.normalize(input_data, dim=0)
input_data = input_data.repeat(3, 6)
result = torch.qr(torch.matmul(input_data.T, input_data))[0]
