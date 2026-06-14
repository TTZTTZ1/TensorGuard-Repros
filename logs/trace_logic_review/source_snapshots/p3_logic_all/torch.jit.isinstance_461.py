
obj = torch.tensor(2)
obj = obj
obj = torch.any((obj == 2))
obj = (obj + torch.Tensor(obj.size()))
target_type = torch.Tensor
result = torch.jit.isinstance(obj, target_type)
type(result)
