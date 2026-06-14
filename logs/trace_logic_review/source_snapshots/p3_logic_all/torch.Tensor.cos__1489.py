
a = torch.rand(10, 3).to(torch.device('cpu'))
a = a.to(torch.device('cpu'))
torch.Tensor.cos_(torch.FloatTensor(a)).to(torch.device('cpu'))
