
_input_tensor = torch.tensor([1.0, float('nan'), 3.0, 4.0])
q = torch.Tensor([0.0])
result = torch.Tensor.nanquantile(_input_tensor, q)
