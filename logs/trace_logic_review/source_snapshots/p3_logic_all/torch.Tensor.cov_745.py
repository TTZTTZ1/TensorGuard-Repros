
cov_matrix = torch.Tensor.cov(torch.randn(10, 10))
(_, P) = torch.linalg.eig(cov_matrix)
P
