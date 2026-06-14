indices = torch.tensor([[0, 1], [2, 3]])
values = torch.tensor([1.0, 2.0])
size = (4, 4)
tensor = torch.sparse_coo_tensor(indices, values, size)