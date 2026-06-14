
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
sparse_tensor = torch.sparse_coo_tensor(torch.tensor(indices), values, torch.Size([3, 3]))
sparse_tensor.indices = torch.tensor([0, 1, 2])
sparse_tensor.dense_data = torch.tensor([4.0, 5.0, 6.0], dtype=torch.float)
