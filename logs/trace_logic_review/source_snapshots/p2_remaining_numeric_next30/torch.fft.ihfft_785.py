
input_data = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32, requires_grad=True)
result = torch.fft.ihfft(input_data, n=2048)
result.requires_grad_(True)
result = torch.fft.fft(result, n=2048)
result = torch.fft.fft(result, n=2048)
result.requires_grad_(True)
result = torch.fft.fft(result, n=2048)
result.requires_grad_(True)
result = torch.fft.fft(result, n=2048)
result = torch.fft.ifft(result, n=2048)
output_data = torch.fft.fft(result, n=2048)
output_data
