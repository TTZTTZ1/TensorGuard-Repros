
x = torch.randn(10)
result = torch.Tensor.mv((torch.eye(10) + 1), x)
(torch.is_tensor(result) is True)
(result.type() == torch.Tensor(result.size()))
(torch.sum(result) == torch.sum(x))
