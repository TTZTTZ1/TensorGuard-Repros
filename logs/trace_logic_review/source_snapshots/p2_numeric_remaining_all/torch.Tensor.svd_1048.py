
_input_tensor = torch.randn(1000, 4)
_input_tensor = torch.tensor(_input_tensor, dtype=torch.float32)
_input_tensor = torch.tensor(_input_tensor).type(torch.FloatTensor)
(U, s, Vh) = torch.Tensor.svd(torch.t(_input_tensor))
