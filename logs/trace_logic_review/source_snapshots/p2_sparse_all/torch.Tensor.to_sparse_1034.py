
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.rand(4, 4))
torch.spmm(input_tensor, output_tensor.t())
torch.mm(input_tensor, output_tensor)
torch.spmm(input_tensor, output_tensor.t())
torch.matmul(input_tensor, output_tensor)
