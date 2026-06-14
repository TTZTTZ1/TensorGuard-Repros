
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
sparse_tensor = torch.sparse_coo_tensor(indices, values, torch.Size([3, 3]))
sparse_tensor.indices = torch.tensor([0, 1, 2])
sparse_tensor.values = torch.ones(3)
sparse_tensor_new = sparse_tensor.to_dense()
