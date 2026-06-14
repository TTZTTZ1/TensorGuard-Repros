
other_data = torch.randn(2, 3, 5, 3)
other_data = torch.Tensor(other_data)
other = (other_data / torch.sum(other_data))
other = (other - other.mean())
other = (other / other.sum())
other = torch.Tensor(other)
torch.Tensor.sub_(torch.tensor(other_data), other)
