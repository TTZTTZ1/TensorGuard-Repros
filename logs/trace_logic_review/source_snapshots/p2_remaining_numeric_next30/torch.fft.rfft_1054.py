
x = torch.arange(100, dtype=torch.float32)
y = torch.sinh(x)
y = torch.cosh(y)
y = torch.exp((- y))
result = torch.fft.rfft(y)
