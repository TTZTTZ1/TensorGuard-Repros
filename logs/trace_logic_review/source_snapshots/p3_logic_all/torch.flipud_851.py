
input_data = torch.Tensor(size=(16, 16)).random_(1, 2)
result = torch.flipud(input_data)
torch.allclose(result, input_data.fliplr())
