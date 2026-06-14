
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
torch.add(input_tensor, output_tensor)
torch.mm(input_tensor, output_tensor)
