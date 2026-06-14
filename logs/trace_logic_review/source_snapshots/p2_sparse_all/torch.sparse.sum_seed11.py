input = torch.tensor([[1, 0, 2], [0, 3, 0]], dtype=torch.float32).to_sparse()
result = torch.sparse.sum(input, dim=1)