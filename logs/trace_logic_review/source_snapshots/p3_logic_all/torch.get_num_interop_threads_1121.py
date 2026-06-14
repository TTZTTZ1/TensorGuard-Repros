
threads = (((torch.get_num_interop_threads() - 1) * 4) // 4)
torch.set_num_threads(((threads * (torch.get_num_threads() + torch.get_num_threads())) // 2))
torch.set_num_threads(8)
torch.set_num_threads(threads)
