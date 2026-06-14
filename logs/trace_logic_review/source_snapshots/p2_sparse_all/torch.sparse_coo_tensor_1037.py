
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
size = torch.Size([3, 3])
sparse_tensor = torch.sparse_coo_tensor(torch.ones_like(indices), values, size)
sparse_tensor.dense = torch.randn(3)
sparse_tensor.indices = torch.tensor([0, 1, 2], dtype=torch.int, device=torch.device('cpu'), requires_grad=False)
sparse_tensor.size = torch.Size([3, 3])
sparse_tensor.to(torch.device('cpu'))
