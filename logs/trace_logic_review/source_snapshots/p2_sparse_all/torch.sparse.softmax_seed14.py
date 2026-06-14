input_data = torch.tensor([[0.5, (- 0.2)], [0.8, 0.1]], dtype=torch.float32)
output = torch.sparse.softmax(input_data.to_sparse(), dim=1)