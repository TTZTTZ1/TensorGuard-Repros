
input_data = torch.randn(2, 3)
input_data = torch.nn.functional.normalize(input_data, dim=0)
input_data = input_data.repeat(3, 6)
result = torch.qr(torch.matmul(input_data, input_data.t()))[0]
result
