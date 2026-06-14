
N = int(100000000.0)
fft_data = torch.arange(N, dtype=torch.float)
result = torch.fft.hfft(fft_data)
result = torch.abs(result)
