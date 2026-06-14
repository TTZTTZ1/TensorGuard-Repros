
device = torch.device('cpu')
torch.Tensor.sgn_(torch.tensor(0.8).to('cpu').unsqueeze(0).to('cpu')).to(device)
