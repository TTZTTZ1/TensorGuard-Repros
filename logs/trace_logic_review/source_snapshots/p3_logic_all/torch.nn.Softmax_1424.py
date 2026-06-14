
input_data = torch.FloatTensor(size=(10, 2))
output = torch.nn.Softmax(dim=1)(input_data)
torch.allclose(input_data, output)
