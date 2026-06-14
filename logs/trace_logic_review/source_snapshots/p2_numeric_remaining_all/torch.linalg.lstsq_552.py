
A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
B = torch.tensor([5.0, 6.0])
solution = torch.linalg.lstsq(A, B, rcond=0.2)[0].unsqueeze((- 1))
torch.allclose(solution, torch.tensor([[6.0, 19.0], [(- 17.0), (- 13.0)]]), atol=1e-05)
