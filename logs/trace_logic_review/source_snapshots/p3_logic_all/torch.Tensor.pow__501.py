
a = np.array([1, 2, 3, 4, 5, 6], dtype=np.float32)
b = torch.from_numpy(a)
torch.Tensor.pow_(torch.Tensor(a), b)
