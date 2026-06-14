
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
output = torch.spmm(input_tensor, output_tensor)
torch.spmm(input_tensor, output_tensor)
torch.spmm(input_tensor, output_tensor.to_sparse())
torch.spmm(input_tensor, output_tensor.to_sparse())
input_tensor = torch.randn(4, 4)
torch.mm(input_tensor, output_tensor)
