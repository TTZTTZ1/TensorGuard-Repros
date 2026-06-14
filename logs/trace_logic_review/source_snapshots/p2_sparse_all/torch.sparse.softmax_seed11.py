indices = torch.tensor([[0, 0], [1, 2]])
values = torch.tensor([0.2, 0.7], dtype=torch.float32)
sparse_tensor = torch.sparse_coo_tensor(indices, values, size=(2, 3))
dim = 1
result = torch.sparse.softmax(sparse_tensor, dim=dim)