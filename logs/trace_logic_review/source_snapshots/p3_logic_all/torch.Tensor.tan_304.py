
_input_tensor = ((torch.randn(3, 5, 224, 224) * 2) - 1)
_input_tensor = torch.Tensor.tan(_input_tensor)
torch.allclose(_input_tensor, torch.tan(_input_tensor))
