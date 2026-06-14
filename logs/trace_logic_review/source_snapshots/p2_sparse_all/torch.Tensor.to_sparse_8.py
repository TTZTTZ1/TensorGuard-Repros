
input_tensor = torch.randn(3, 4)
output_tensor = torch.Tensor.to_sparse(torch.Tensor([1])).to(input_tensor)
