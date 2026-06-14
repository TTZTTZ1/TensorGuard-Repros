
input_data = torch.FloatTensor(np.random.uniform((- 1), 1, (3, 4)))
input_data = torch.nn.functional.normalize(input_data, dim=0)
input_data = input_data.repeat(3, 6)
result = torch.qr(torch.mm(input_data, input_data.t()))
result = result[0]
