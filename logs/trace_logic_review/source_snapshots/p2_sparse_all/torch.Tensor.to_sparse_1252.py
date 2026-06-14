
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
input_tensor.requires_grad_(True)
output_tensor.requires_grad_(True)
