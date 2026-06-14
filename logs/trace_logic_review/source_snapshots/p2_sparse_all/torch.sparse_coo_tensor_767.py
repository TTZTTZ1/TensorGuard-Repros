
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
size = torch.Size([3, 3])
sparse_tensor = torch.sparse_coo_tensor(torch.ones_like(indices), values, size, device=torch.device('cpu'))
sparse_tensor.sort_indices = torch.tensor([1, 0, 0], dtype=torch.int, device=torch.device('cpu'))
sparse_tensor.format = torch.sparse_coo_tensor
sparse_tensor.indices = torch.tensor([0, 1, 2], dtype=torch.int, device=torch.device('cpu'))
sparse_tensor.dense_shape = torch.Size([3, 1])
