
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4))
torch.mm(input_tensor, output_tensor)
torch.spmm(input_tensor, output_tensor.t())
torch.matmul(input_tensor, output_tensor)
torch.spmm(output_tensor, input_tensor.t())
