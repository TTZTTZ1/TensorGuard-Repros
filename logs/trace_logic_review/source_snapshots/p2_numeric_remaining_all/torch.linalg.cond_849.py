
A = np.ones((3, 3, 2))
A = torch.tensor(A)
result = torch.linalg.cond(A)
result.shape
