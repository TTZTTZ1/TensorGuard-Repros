
input_tensor = torch.randn(2, 3)
output_tensor = torch.Tensor.transpose(torch.argsort(input_tensor), 0, 1)
torch.set_printoptions(precision=2)
torch.set_num_threads(2)
torch.set_grad_enabled(False)
torch.autograd.set_detect_anomaly(True)
output = torch.argsort(output_tensor)
output = output[0]
output = torch.sort(output_tensor)
