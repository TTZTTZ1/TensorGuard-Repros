
input_tensor = torch.randn(8, 4)
output_tensor = torch.randn(8, 4)
output_tensor = torch.Tensor.to_sparse(output_tensor)
torch.spmm(input_tensor, output_tensor.t())
