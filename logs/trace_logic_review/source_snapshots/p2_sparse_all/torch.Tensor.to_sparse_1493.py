"""
{"exception": "TypeError", "msg": "invalid type object: only floating-point types are supported as the default type"}
"""

input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
torch.set_default_tensor_type(torch.tensor)
torch.mm(input_tensor, output_tensor)
