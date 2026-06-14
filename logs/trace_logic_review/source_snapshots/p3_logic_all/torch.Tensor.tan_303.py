
_input_tensor = torch.randn(5, 3, 224, 224)
_input_tensor = torch.Tensor.tan(_input_tensor)
_tensor_tensor_2 = torch.tan(_input_tensor)
torch.allclose(_input_tensor, torch.tan(_input_tensor))
