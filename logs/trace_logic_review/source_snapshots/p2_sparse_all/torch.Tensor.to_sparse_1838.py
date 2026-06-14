
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
output = torch.spmm(input_tensor, output_tensor)
output.requires_grad_(True)
input_tensor = torch.rand(3, 4)
torch.mm(input_tensor, output_tensor)
