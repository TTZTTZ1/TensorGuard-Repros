
_input_tensor = torch.randn(2, 5, 20)
(U, s, Vh) = torch.Tensor.svd(torch.Tensor(_input_tensor), some=True)
