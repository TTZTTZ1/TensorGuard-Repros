
x = torch.arange(100, dtype=torch.float32)
y = ((x * 2) + 3)
y = ((y * 2) - 1)
y = torch.cosh(y)
y = torch.exp((- y))
result = torch.fft.rfft(y)
