
input_tensor = torch.randn(3, 3, 3, 64).type(torch.FloatTensor)
input_tensor = input_tensor.to('cpu')
output_tensor = torch.Tensor.type_as(input_tensor, torch.FloatTensor())
input_tensor += output_tensor
input_tensor = torch.sign(input_tensor)
input_tensor = torch.abs(input_tensor)
input_tensor = torch.clamp(input_tensor, min=(- 1), max=1)
