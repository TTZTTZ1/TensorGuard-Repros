
device = torch.device('cpu')
data = torch.rand(10, 1, requires_grad=True)
result = torch.Tensor(torch.zeros(10, 1).to(device))
result = torch.Tensor.add_(result, data)
result = torch.Tensor.add_(result, 5)
result = torch.Tensor.add_(result, 12)
result = torch.Tensor.add_(result, 9)
