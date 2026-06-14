
input_tensor = torch.randn(4, 3)
input_tensor = torch.autograd.Variable(input_tensor)
input_tensor = torch.autograd.Variable(torch.FloatTensor(*input_tensor.shape))
prelu = torch.nn.PReLU()
output_tensor = prelu(input_tensor)
output = prelu(input_tensor)
