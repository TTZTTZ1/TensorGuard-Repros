
input_tensor = torch.Tensor([[1, 2], [3, 4]])
output_tensor = torch.Tensor.new_zeros(input_tensor, (2, 2), dtype=torch.int32)
output_tensor = torch.zeros_like(output_tensor)
output_tensor = torch.cat((output_tensor, input_tensor), 1)
output_tensor = torch.LongTensor(output_tensor.size())
