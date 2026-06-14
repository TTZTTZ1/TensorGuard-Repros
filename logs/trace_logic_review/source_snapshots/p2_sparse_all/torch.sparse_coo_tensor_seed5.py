indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3, 4, 5])
size = (3, 3)
sparse_tensor = torch.sparse_coo_tensor(indices, values, size)