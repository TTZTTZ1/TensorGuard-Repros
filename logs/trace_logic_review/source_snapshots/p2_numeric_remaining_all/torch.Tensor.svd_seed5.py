_input_tensor = torch.randn(5, 5)
(u, s, vh) = torch.Tensor.svd(_input_tensor, some=True, compute_uv=True)