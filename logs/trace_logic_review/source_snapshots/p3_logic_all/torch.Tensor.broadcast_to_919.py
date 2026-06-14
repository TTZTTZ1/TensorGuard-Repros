
shape = (3, 2)
result = torch.Tensor.broadcast_to(torch.tensor([1, 2]), shape)
assert (result.size() == (3, 2))
result[0] = 0.0
result = result.to('cpu')
assert (result.size() == (3, 2))
result[0] = 1.0
result = result.to('cpu')
assert (result.size() == (3, 2))
torch.set_printoptions(threshold=4)
result = result.to('cpu')
assert (result.size() == (3, 2))
