indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
sparse_matrix = torch.sparse_coo_tensor(indices, values, size=(2, 3))
result = torch.sparse.sum(sparse_matrix, dim=1)