
input_tensor = torch.randn(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.randn(4, 4))
torch.spmm(input_tensor, output_tensor.t())
