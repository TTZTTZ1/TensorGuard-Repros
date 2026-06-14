
input_tensor = torch.rand([3, 3], dtype=torch.float32)
transform = torch.distributions.transforms.CorrCholeskyTransform()
result = transform(input_tensor)
result = result.to_sparse()
input_tensor = torch.matmul(input_tensor, result.to_dense())
