
_input_tensor = torch.randn(8, 4, 3).float()
(U, s, Vh) = torch.Tensor.svd(_input_tensor, compute_uv=True)
