
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
size = torch.Size([3, 3])
sparse_tensor = torch.sparse_coo_tensor(torch.ones_like(indices), values, size)
sparse_indices = torch.arange(3)
sparse_indices_2d = torch.stack([sparse_indices, sparse_indices], dim=0)
sparse_tensor.dense_shape = torch.Size([3, 1])
