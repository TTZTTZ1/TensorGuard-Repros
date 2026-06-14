
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0], dtype=torch.float)
sparse_tensor = torch.sparse_coo_tensor(indices=torch.LongTensor(indices), values=torch.FloatTensor(values))
sparse_tensor.indices = torch.tensor([0, 2, 1])
sparse_tensor.values = torch.tensor([10.0, 20.0, 30.0, 40.0], dtype=torch.float)
