
_input_tensor = torch.from_numpy(np.random.random_sample(1000)).float()
_input_tensor = torch.autograd.Variable(torch.FloatTensor(_input_tensor.size()))
_input_tensor = _input_tensor.to(torch.double)
_input_tensor = (_input_tensor / torch.sum(_input_tensor))
_input_tensor = torch.autograd.Variable(_input_tensor).to(torch.double)
result = torch.Tensor.corrcoef(_input_tensor)
result.shape
