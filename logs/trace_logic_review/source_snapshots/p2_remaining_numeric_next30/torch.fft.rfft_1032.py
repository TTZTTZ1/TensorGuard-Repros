
x = torch.arange(0, 10000, dtype=torch.float)
y = (torch.exp((- x)) / (x ** 2))
result = torch.fft.rfft(y)
