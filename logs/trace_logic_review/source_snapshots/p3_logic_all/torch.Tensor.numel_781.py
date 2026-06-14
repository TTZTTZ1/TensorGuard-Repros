
_input_tensor = torch.rand(8, 3, 3, 3, dtype=torch.float32)
_input_tensor = _input_tensor.permute(0, 3, 1, 2)
_output_tensor = (((torch.Tensor.numel(_input_tensor) * 3) + ((torch.Tensor(_input_tensor.size()) * 3) + (torch.tensor([(- 1)]) * torch.numel(_input_tensor)))) + 1)
