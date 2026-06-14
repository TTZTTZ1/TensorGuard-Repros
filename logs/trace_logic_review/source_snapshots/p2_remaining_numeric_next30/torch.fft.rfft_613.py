
x = torch.arange(100).reshape(10, 10)
y = torch.exp(x)
result = torch.fft.rfft(y)
result = torch.fft.irfft(result)
