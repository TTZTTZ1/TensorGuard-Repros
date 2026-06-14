
input = torch.arange(1, 32000, dtype=torch.float)
n_fft = 512
hop_length = 256
win_length = None
window = torch.hann_window(n_fft)
center = True
pad_mode = 'reflect'
normalized = False
onesided = None
return_complex = True
stft_result = torch.stft(input, n_fft, hop_length, win_length, window, center, pad_mode, normalized, onesided, return_complex)
