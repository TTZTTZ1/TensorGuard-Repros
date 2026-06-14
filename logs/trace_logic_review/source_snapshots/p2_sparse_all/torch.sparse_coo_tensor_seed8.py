indices = torch.tensor([[0, 1], [2, 3]])
values = torch.tensor([1.0, 2.0])
size = torch.Size([4, 1])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size)