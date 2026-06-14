
input_tensor = torch.sparse_coo_tensor(torch.as_tensor([[0, 1, 1], [2, 0, 2]], dtype=torch.int64), torch.tensor([3, 4, 5]), size=(2, 3))
result = torch.sparse.sum(input_tensor)
result
result
result = result
result
result = result.to_dense()
