
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
(output_tensor, input_tensor)
