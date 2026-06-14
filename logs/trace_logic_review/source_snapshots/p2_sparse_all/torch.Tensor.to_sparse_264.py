
output_tensor = torch.Tensor.to_sparse(torch.randn(4, 4))
output_tensor.to_dense()
