
input_tensor = torch.randn(5, 3, 10)
indices = torch.arange(5, dtype=torch.long, device=torch.device('cpu'))
result = torch.take_along_dim(input_tensor, indices, out=torch.ones(3, 1))
result.detach_()
result = result.detach()
