
_input_tensor = torch.tensor([[4.0, 6.0], [0.0, 5.0]]).float()
pinverse_result = torch.Tensor.pinverse(_input_tensor)
result = torch.cat((_input_tensor, torch.div(pinverse_result, _input_tensor)), dim=0)
