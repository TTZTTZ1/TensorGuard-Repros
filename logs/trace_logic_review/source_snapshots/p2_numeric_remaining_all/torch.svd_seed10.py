input = torch.randn(5, 3)
(U, S, Vh) = torch.svd(input, some=True, compute_uv=True)