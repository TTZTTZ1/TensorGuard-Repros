
fft_data = torch.arange(0, 1024, 0.1)
result = torch.fft.hfft(fft_data)
result = torch.abs(result)
