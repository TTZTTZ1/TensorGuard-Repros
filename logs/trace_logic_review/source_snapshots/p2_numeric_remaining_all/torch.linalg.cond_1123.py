
A = torch.tensor(torch.diag(torch.arange(0, 10))).float()
A = torch.add(A, A.T)
A = torch.tensor(A)
A = torch.exp(A)
result = torch.linalg.cond(A)
result.shape
