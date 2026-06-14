
indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
size = torch.Size([3, 3])
sparse_tensor = torch.sparse_coo_tensor(torch.ones_like(indices), values, size)
torch.set_printoptions(edgeitems=None)
sparse_tensor.indices = torch.tensor([0, 1, 2], dtype=torch.int, device=torch.device('cpu'), requires_grad=False)
sparse_tensor.values = torch.tensor([1.0, 2.0, 3.0], dtype=torch.double, device=torch.device('cpu'))
sparse_tensor.size = torch.Size([2, 3])
