_input_tensor = torch.randn(5, 5)
(U, S, Vt) = torch.Tensor.svd(_input_tensor)