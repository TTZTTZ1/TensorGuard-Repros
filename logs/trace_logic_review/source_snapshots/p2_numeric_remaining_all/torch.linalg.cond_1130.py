
A = torch.tensor(torch.diag(torch.arange(0, 10))).float()
A = torch.add(A, A.T)
A = torch.tensor(A)
A = (A * torch.randn(*A.shape))
result = torch.linalg.cond(A)
result.shape
