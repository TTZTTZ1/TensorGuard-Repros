
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
size = torch.Size([3, 3])
sparse_tensor = torch.sparse_coo_tensor(indices, values, torch.Size([2, 2]))
sparse_tensor.dense_shape = torch.Size([2])
sparse_tensor.dense_shape = size
