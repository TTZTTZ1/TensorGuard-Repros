
other_data = torch.randn(2, 3, 5, 3)
other = torch.Tensor.sub_(torch.Tensor(other_data).mean(dim=0), torch.Tensor(other_data).std())
other = (other - other.mean())
other = (other / other.sum())
