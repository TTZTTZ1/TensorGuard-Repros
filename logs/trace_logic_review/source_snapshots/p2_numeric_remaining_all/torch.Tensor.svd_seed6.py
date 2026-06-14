_input_tensor = torch.randn(3, 4)
(U, S, Vh) = torch.Tensor.svd(_input_tensor, some=True, compute_uv=True)