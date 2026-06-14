
x = torch.arange((2 ** 16)).view(2, (- 1)).type(torch.FloatTensor)
result = torch.fft.fftshift(torch.fft.fft(x))
result = torch.fft.ifft(result)
result = torch.fft.fftshift(result)
y = result
result = torch.fft.ifft(y)
result = torch.fft.ifftn(result)
result1 = torch.fft.fftshift(result)
result2 = torch.fft.ifftshift(result)
