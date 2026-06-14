
A = torch.tensor([[0.0, 0.0, 1.0, 2.0], [0.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 2.0], [0.0, 0.0, 1.0, 2.0]])
result = torch.linalg.cond(A)
result.shape
