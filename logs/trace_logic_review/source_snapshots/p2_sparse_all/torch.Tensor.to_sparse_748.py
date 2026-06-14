
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.tensor(input_tensor))
torch.spmm(input_tensor, output_tensor.t())
torch.spmm(input_tensor, output_tensor.t())
