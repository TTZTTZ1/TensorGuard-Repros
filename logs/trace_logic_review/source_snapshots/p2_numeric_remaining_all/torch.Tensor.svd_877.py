
_input_tensor = torch.randn(1000, 4)
_input_tensor = torch.tensor(_input_tensor, dtype=torch.float32)
_input_tensor = torch.tensor(_input_tensor).type(torch.FloatTensor)
_input_tensor = torch.tensor(_input_tensor, requires_grad=True)
_input_tensor = torch.tensor(_input_tensor).type(torch.FloatTensor)
(U, s, Vh) = torch.Tensor.svd(_input_tensor, some=False)
