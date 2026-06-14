
x = torch.arange(0, 10000, dtype=torch.float)
y = torch.exp(x)
result = torch.fft.rfft(y)
