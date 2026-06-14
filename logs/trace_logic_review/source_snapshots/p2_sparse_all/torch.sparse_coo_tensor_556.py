
sparse_tensor = torch.sparse_coo_tensor(torch.IntTensor([0]), torch.IntTensor([0]), torch.IntTensor([0]))
sparse_tensor.indices = torch.tensor([0, 1, 2])
