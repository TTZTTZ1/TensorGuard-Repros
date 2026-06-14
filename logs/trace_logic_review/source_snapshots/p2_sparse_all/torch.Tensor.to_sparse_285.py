
input_tensor = torch.randn(8, 4)
output_tensor = torch.randn(16, 4)
output_tensor = torch.Tensor.to_sparse(output_tensor)
input_tensor = torch.Tensor(input_tensor)
torch.spmm(input_tensor, output_tensor.t())
