input = torch.tensor([[0.2, 0.1, 0.7], [0.6, 0.2, 0.2]], requires_grad=True)
dim = 1
result = torch.sparse.softmax(input.to_sparse(), dim=dim)