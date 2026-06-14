
tensor = torch.rand(4, 4)
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(tensor.t())
torch.spmm(input_tensor, output_tensor.t())
