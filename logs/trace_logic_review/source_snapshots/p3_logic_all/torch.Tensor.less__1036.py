
input = 123
other = torch.tensor(1)
input_tensor = torch.Tensor(input)
output_tensor = torch.Tensor.less_(input_tensor, other)
output_tensor
