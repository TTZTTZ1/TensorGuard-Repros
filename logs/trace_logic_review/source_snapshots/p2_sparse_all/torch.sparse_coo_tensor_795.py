
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0], dtype=torch.float)
torch.sparse_coo_tensor(indices=torch.LongTensor(indices), values=torch.FloatTensor(values)).indices
