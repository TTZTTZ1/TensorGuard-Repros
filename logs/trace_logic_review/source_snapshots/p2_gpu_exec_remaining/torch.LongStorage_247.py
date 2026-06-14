
data = torch.LongTensor([1, 2, 3])
result = torch.LongStorage(data.size()[0])
data[0] = 100
result[1] = 200
