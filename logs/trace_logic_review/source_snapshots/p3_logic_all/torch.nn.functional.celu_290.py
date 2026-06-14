
input_data = torch.tensor([(- 2.0), (- 1.0), 0.0, 1.0, 2.0])
output = torch.nn.functional.celu(torch.autograd.Variable(torch.Tensor(input_data.size())))
