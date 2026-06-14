
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0], dtype=float)
sparse_tensor = torch.sparse_coo_tensor(indices=indices, values=values, size=[4, 4])
sparse_tensor.indices = torch.tensor([0, 1])
sparse_tensor.indptr = ([0, 3], [2, 2])
