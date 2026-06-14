
_input_tensor = torch.randn(4, 3, 10, 32).type(torch.FloatTensor)
_input_tensor = torch.tensor(_input_tensor, requires_grad=True)
_input_tensor = torch.tensor(_input_tensor).type(torch.FloatTensor)
(U, s, Vh) = torch.Tensor.svd(_input_tensor.view(4, 3, 10, 32))
