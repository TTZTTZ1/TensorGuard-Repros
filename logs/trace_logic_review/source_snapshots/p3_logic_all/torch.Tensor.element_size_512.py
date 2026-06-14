
_input_tensor = torch.randn(1, 3, 224, 224, dtype=torch.float32)
_result = torch.Tensor(torch.Tensor.element_size(_input_tensor)).zero_()
