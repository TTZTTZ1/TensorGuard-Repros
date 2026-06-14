
window_length = 10
N = 128
input_data = torch.Tensor(N, window_length)
result = torch.bartlett_window(window_length, periodic=True, dtype=input_data.dtype)
input_data_double = input_data.double()
result_double = result.double()
