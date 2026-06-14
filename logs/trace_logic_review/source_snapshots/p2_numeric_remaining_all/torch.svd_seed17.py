input_tensor = torch.randn(5, 5)
(U, S, Vh) = torch.svd(input_tensor, some=True, compute_uv=True)