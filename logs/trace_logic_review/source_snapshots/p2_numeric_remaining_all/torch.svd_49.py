
input_tensor = torch.randn(5, 3)
(U, S, Vh) = torch.svd(input_tensor)
