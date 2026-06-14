
other_data = torch.randn(2, 3, 5, 3)
other = (other_data * torch.Tensor(other_data.shape))
other = (other / other.sum())
other = torch.Tensor(other)
torch.Tensor.sub_(other, (other.sum() / other.numel()))
