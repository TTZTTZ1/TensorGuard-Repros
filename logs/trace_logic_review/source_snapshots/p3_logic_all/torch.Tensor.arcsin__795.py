
x = 2
y = np.pi
result = torch.Tensor.arcsin_((torch.Tensor(x) * y))
torch.allclose(result, torch.from_numpy(np.array([2, np.pi])).float())
