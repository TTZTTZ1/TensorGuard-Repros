
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
output = torch.spmm(input_tensor, output_tensor)
assert torch.is_tensor(output)
assert output.shape
