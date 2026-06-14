input_tensor = torch.tensor([[0.5, (- 0.1), 0.7], [(- 0.8), 0.3, 0.2]], dtype=torch.float32)
dim = 1
result = torch.sparse.softmax(input_tensor.to_sparse(), dim=dim)