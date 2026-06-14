
input_tensor = torch.randn(10)
chunks = 5
result = torch.Tensor.chunk(torch.Tensor(input_tensor.size()), chunks)
