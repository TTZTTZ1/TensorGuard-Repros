
A = np.ones((2, 2))
A = torch.tensor(A)
result = torch.linalg.cond(A)
result.shape
