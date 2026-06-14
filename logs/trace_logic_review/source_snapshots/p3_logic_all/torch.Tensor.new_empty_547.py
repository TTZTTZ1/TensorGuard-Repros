
input_tensor = torch.Tensor(size=(2, 2))
input_tensor = torch.nn.Parameter(input_tensor, requires_grad=True)
output_tensor = torch.Tensor.new_empty(input_tensor, size=(2, 2))
output_tensor.requires_grad = True
