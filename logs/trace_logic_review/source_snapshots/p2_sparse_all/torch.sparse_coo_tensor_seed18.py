indices = torch.tensor([[0, 1], [2, 3]], dtype=torch.long)
values = torch.tensor([4.0, 5.0], dtype=torch.float32)
size = (4, 4)
sparse_tensor = torch.sparse_coo_tensor(indices, values, size)