
input = torch.autograd.Variable(torch.zeros(4, 3))
input = torch.autograd.Variable(input, requires_grad=True)
input = torch.autograd.Variable(input)
tau = torch.rand(3)
result = torch.orgqr(input, tau)
result[1:] = result[1:].T
