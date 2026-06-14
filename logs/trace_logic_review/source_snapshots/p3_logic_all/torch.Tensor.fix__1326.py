
input_tensor = torch.Tensor(np.array([1.5, (- 2.3)]))
_input_tensor = torch.FloatTensor([1.5, (- 2.3)])
_input_tensor = _input_tensor.to('cpu')
_input_tensor_requires_grad = torch.Tensor(_input_tensor)
torch.Tensor.fix_(_input_tensor_requires_grad)
with torch.no_grad():
    y = torch.nn.functional.l1_loss(_input_tensor, torch.Tensor(_input_tensor.shape))
assert y
