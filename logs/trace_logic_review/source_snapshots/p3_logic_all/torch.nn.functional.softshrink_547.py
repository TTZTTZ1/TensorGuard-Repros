
input_data = torch.ones(10, 10).type(torch.FloatTensor)
output = torch.nn.functional.softshrink(torch.Tensor(input_data.T), 0)
torch.Size([10, 10])
output
(output, input_data)
(output, torch.Tensor(input_data.size()))
(output, torch.sin(input_data))
(output, torch.cos(input_data))
(output, torch.tan(input_data))
(output, torch.softmax(input_data, dim=(- 1)))
