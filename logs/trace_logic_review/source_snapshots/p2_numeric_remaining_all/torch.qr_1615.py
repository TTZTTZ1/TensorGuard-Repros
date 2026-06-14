
input_data = torch.ones(3, 5, requires_grad=True)
input_data = torch.nn.functional.normalize(input_data, dim=0)
input_data = input_data.repeat(3, 6)
result = torch.qr(torch.mm(input_data, torch.transpose(input_data, 1, 0)))[0]
