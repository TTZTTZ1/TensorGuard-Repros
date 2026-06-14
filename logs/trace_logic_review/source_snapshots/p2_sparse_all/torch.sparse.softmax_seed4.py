indices = torch.tensor([[0, 0], [1, 2]])
values = torch.tensor([0.5, 0.7], dtype=torch.float32)
sparse_input = torch.sparse_coo_tensor(indices, values, size=(2, 3))
dim = 1
output = torch.sparse.softmax(sparse_input, dim=dim)