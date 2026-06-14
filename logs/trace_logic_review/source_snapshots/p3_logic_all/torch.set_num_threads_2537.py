
num_threads = int(((torch.get_num_threads() - 1) * torch.ones(torch.Size())))
num_threads = int(torch.min(torch.as_tensor([num_threads], dtype=torch.int64).view((- 1))))
num_threads = torch.as_tensor(num_threads).view(1, (- 1)).item()
torch.set_num_threads(num_threads)
