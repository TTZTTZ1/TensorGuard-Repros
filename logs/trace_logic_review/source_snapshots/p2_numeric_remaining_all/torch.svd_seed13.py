input_data = torch.randn(5, 5)
(U, S, Vh) = torch.svd(input_data, some=True, compute_uv=True)