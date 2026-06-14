
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.eye(4, device=torch.device('cpu')))
output = torch.spmm(input_tensor, output_tensor)
input = torch.sparse.FloatTensor(4, 4).to(input_tensor.device)
output
torch.sparse.mm(input_tensor, output_tensor)
torch.sparse.mm(input_tensor, output_tensor.t())
output
torch.mm(input_tensor, output_tensor)
