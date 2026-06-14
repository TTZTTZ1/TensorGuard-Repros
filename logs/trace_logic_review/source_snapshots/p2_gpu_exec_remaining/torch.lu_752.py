
A = torch.tensor([[4.0, 3.0], [6.0, 3.0]])
(lu, pivots) = torch.lu(A, pivot=True, get_infos=False)
(lu, pivots)
