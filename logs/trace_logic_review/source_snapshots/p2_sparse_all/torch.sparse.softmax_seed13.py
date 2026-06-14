indices = torch.tensor([[0, 0], [1, 1]])
values = torch.tensor([0.2, 0.7], dtype=torch.float32)
size = (2, 2)
sparse_input = torch.sparse_coo_tensor(indices, values, size)
dim = 1
output = torch.sparse.softmax(sparse_input, dim=dim)