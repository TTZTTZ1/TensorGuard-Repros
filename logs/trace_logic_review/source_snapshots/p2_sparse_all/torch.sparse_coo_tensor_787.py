
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0], requires_grad=True)
sparse_coo_tensor = torch.sparse_coo_tensor(indices, values)
