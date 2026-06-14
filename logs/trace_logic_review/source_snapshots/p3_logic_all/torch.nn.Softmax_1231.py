
input = torch.randn(10, 3)
input_data = torch.Tensor(input.size())
output = torch.nn.Softmax(dim=1)(input)
torch.allclose(input_data, output)
