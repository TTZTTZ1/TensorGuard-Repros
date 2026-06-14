
_input_tensor = torch.ones(1, 4)
_input_tensor = torch.autograd.Variable(torch.FloatTensor(_input_tensor.size()))
_input_tensor = _input_tensor.to(torch.double)
_input_tensor = (_input_tensor / torch.sum(_input_tensor))
_input_tensor = torch.autograd.Variable(_input_tensor).to(torch.double)
result = torch.Tensor.corrcoef(_input_tensor)
result.shape
