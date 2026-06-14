
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
size = torch.Size([3, 3])
sparse_tensor = torch.sparse_coo_tensor(torch.tensor(indices), torch.tensor(values), torch.Size(size))
sparse_tensor.indices = torch.tensor([0, 1, 2])
