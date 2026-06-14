
A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
B = torch.tensor([5.0, 6.0])
solution = torch.linalg.lstsq(A, B, True)
solution = solution[0]
