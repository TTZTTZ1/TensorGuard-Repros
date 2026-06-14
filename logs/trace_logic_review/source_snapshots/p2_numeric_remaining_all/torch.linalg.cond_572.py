
A = torch.arange(((3 * 4) * 5), dtype=torch.float32).reshape((3, 4, 5))
A = torch.tensor(A)
result = torch.linalg.cond(A, 2)
result = torch.tensor(result)
result.shape
result.shape
