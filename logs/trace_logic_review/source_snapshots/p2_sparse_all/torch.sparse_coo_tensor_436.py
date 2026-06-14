
size = torch.Size([3, 3])
sparse_tensor = torch.sparse_coo_tensor(size)
sparse_tensor.indices = torch.tensor([0, 1, 2])
