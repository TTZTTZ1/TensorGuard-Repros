
input_tensor = torch.FloatTensor([[1, 2, 3, 4], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4], [1, 2, 3, 4]])
output_tensor = torch.Tensor.to_sparse(torch.eye(4, 4))
torch.spmm(input_tensor, output_tensor.t())
