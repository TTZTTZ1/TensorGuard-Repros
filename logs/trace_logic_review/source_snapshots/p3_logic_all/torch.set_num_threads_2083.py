
num_threads = int((((torch.get_num_threads() * torch.ones((1,)).view((- 1))[0]) + 1) / torch.get_num_threads()))
num_threads = torch.as_tensor(num_threads).view(1, (- 1)).item()
torch.set_num_threads(num_threads)
