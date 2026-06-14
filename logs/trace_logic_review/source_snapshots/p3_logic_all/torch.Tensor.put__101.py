
input_tensor = torch.rand(size=[2, 3], dtype=torch.float32)
index = torch.tensor([[0, 1], [1, 2]])
source = torch.tensor([[0.1, 0.2], [0.3, 0.4]])
output_tensor = torch.Tensor.put_(input_tensor, index, source, accumulate=False)
output = output_tensor.clone()
