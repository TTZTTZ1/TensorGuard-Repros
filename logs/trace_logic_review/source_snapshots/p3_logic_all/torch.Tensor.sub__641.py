
other_data = torch.randn(2, 3, 5, 3)
other_data = other_data.reshape((- 1), 3, 5, 1)
other = (other_data / torch.sum(other_data))
other = (other - other.mean())
other = (other / other.sum())
other = torch.Tensor(other)
torch.Tensor.sub_(other, other_data)
