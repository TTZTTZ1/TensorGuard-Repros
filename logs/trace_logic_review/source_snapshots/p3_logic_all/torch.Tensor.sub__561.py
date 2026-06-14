
other_data = torch.randn(2, 3, 5, 3)
other = (other_data / torch.sum(other_data))
other = (other - other.mean())
other = (other / other.sum())
other = torch.Tensor(other)
torch.Tensor.sub_(other, other).cpu()
