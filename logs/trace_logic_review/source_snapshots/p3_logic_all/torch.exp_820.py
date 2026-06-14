
input_data = torch.linspace((- 4), 4, 1000)
result = ((- 1) + torch.erf(input_data))
result = (result.sum() / result.numel())
result = (torch.exp(result) / torch.sum(input_data))
