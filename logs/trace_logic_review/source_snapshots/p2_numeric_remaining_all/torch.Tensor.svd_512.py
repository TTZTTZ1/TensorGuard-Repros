
_input_tensor = torch.randn(5, 3, 224, 224).type(torch.FloatTensor)
(U, s, Vh) = torch.Tensor.svd(torch.Tensor(_input_tensor), some=False)
