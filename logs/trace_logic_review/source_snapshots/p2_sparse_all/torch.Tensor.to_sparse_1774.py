
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
output = torch.spmm(input_tensor, output_tensor)
output
torch.sparse.mm(input_tensor, output_tensor)
input_tensor.to_dense()
output_tensor.to_dense()
output
torch.mm(input_tensor, output_tensor)
