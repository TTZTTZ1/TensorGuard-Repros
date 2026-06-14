
input_tensor = torch.sparse_coo_tensor(torch.as_tensor([[0, 1, 1], [1, 2, 0]], dtype=torch.int64), torch.tensor([3, 4, 5]), size=(2, 3))
result = torch.sparse.sum(input_tensor)
result = torch.tensor(result)
result = result.to_dense()
result.require_grad = True
