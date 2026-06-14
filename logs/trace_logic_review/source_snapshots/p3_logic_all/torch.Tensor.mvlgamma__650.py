
_input_tensor = torch.tensor(torch.rand(16, 4, 64, 64)).unsqueeze(dim=0)
p = 3
_input_tensor = (_input_tensor * p)
_input_tensor = torch.sum(((_input_tensor - torch.zeros_like(_input_tensor)) ** 2), dim=0)
_input_tensor = (_input_tensor / torch.sum(torch.exp(_input_tensor), dtype=torch.float))
_input_tensor = torch.mean(torch.exp(_input_tensor), dim=0)
torch.Tensor.mvlgamma_(_input_tensor, p)
