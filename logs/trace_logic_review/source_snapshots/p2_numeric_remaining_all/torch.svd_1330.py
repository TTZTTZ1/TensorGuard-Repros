
input_tensor = torch.randn(3, 3)
(_, s, v) = torch.svd(input_tensor)
