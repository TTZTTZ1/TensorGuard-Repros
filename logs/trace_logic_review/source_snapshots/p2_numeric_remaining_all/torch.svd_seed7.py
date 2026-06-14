input = torch.randn(5, 5)
(U, S, Vh) = torch.svd(input, some=True, compute_uv=True)