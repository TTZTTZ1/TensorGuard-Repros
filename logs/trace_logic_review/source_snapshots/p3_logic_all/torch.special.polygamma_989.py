
n = 20
input_data = (torch.arange(((2 * n) - 1)) / n)
input_data -= input_data.max()
result = torch.special.polygamma(n, input_data)
