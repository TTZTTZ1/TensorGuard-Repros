
device = torch.device('cpu')
input_tensor = torch.arange(0, 16).reshape((4, 4)).to(device)
value = (- 1.0)
result = torch.nn.Threshold(0, value, inplace=True).forward(input_tensor)
