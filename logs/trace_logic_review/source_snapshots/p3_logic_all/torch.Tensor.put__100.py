
input_tensor = torch.rand(3, 4, 2)
index = torch.tensor([[0, 1], [1, 2]])
source = torch.tensor([[0.1, 0.2], [0.3, 0.4]])
output_tensor = torch.Tensor.put_(input_tensor, index, source, accumulate=False)
output = output_tensor.clone()
