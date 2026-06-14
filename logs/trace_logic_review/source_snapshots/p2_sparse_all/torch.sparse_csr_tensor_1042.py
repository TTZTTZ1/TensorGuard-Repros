
row_indices = torch.arange(4, dtype=torch.int64).long()
col_indices = torch.tensor([0, 2, 1, 3])
values = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, device=torch.device('cpu'))
sparse_tensor = torch.sparse_csr_tensor(row_indices, col_indices, values, torch.Size([2, 2]))
m = torch.randn(2, 3)
torch.mm(sparse_tensor, torch.eye(2))
torch.mm(sparse_tensor, m)
torch.mm(sparse_tensor, torch.eye(2).t())
