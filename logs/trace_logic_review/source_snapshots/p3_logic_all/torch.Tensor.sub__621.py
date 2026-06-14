
other_data = torch.randn(2, 3, 5, 3)
other_data = other_data.view(1, 2, 3, 5, 3)
other_data = (other_data - other_data.mean())
other = (other_data / torch.sum(other_data))
other = (other - other.mean())
other = (other / other.sum())
other = torch.Tensor(other)
torch.Tensor.sub_(other_data, other).cpu()
