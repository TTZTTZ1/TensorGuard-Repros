
input_tensor = torch.sparse_coo_tensor(torch.tensor([[0, 1, 1], [2, 0, 2]], dtype=torch.long), torch.tensor([3, 4, 5]))
result = torch.sparse.sum(input_tensor, dim=0)
