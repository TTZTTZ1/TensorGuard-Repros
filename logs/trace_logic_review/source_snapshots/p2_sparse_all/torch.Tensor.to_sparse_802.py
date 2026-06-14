
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4))
torch.spmm(input_tensor, (output_tensor.t() @ input_tensor.t()))
