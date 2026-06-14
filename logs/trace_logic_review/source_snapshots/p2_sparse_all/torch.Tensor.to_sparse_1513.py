
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
torch.spmm(input_tensor, output_tensor)
(input_tensor, output_tensor) = (output_tensor.to(input_tensor), input_tensor.to(input_tensor))
torch.mm(input_tensor, output_tensor)
