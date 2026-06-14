
indices = torch.tensor([[0, 0, 1, 1], [0, 1, 0, 1]])
values = torch.tensor([0.5, 0.4, 0.2, 0.8])
size = torch.Size([2, 2])
input_sparse = torch.sparse_coo_tensor(indices, values, size, requires_grad=True, dtype=torch.float32)
input_sparse = torch.sparse.softmax(input_sparse, dim=1)
input_sparse = torch.sparse.log_softmax(input_sparse, dim=1)
for input_tensor in [input_sparse, input_sparse, input_sparse]:
    print(input_tensor)
