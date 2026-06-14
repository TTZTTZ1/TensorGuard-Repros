
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
input_tensor = torch.tensor([[1, 2, 3, 4]], dtype=torch.float32, device=torch.device('cpu'))
torch.mm(input_tensor, output_tensor)
