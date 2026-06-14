
input_tensor = torch.ones(4, 4)
output_tensor = torch.Tensor.to_sparse(torch.FloatTensor(input_tensor))
torch.spmm(output_tensor, input_tensor)
