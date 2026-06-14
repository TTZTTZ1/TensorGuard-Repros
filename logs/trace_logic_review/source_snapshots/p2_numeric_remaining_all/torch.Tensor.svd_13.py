
_input_tensor = torch.randn(5, 3)
(U, s, Vh) = torch.Tensor.svd(_input_tensor)
