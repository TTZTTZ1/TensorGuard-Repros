input = torch.tensor([[0.5, (- 0.2)], [0.1, 0.8]])
dim = 1
result = torch.sparse.softmax(input.to_sparse(), dim=dim)