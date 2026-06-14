
input_tensor = torch.sparse_coo_tensor(torch.tensor([[0, 1, 1], [2, 0, 2]]), torch.tensor([3, 4, 5]), size=(2, 3))
result = torch.sparse.sum(input_tensor, dim=1)
result = result.to
