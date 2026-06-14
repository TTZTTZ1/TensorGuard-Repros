
window_length = 51
result = torch.kaiser_window(window_length, periodic=True, beta=12.0, dtype=torch.float32)
window_result = torch.as_tensor(result, dtype=torch.float32)
torch.allclose(result.to('cpu'), window_result.cpu())
window_result[:window_length] = 0.0
assert (torch.all((result < window_length)), result)
