
input_tensor = torch.sparse_coo_tensor(torch.tensor([[0, 1, 0], [1, 2, 0]], dtype=torch.int64), torch.tensor([3, 4, 0]), size=(3, 2))
result = torch.sparse.sum(input_tensor, dim=0)
