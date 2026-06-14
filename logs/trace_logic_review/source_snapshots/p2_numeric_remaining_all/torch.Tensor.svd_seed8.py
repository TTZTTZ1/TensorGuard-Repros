_input_tensor = torch.randn(5, 5)
(U, S, Vh) = torch.Tensor.svd(_input_tensor, some=True, compute_uv=True)