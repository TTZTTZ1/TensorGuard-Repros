indices = torch.tensor([[0, 1], [2, 3]])
values = torch.tensor([4.0, 5.0])
size = torch.Size([4, 4])
sparse_tensor = torch.sparse_coo_tensor(indices, values, size)