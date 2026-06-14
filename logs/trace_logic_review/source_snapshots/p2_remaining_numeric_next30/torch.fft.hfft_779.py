
fft_data = torch.arange((2 ** 13))
result = torch.fft.hfft(fft_data)
result = torch.abs(result)
