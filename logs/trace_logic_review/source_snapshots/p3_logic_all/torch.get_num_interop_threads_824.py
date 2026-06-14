
threads = (((torch.get_num_interop_threads() == 0) or (torch.get_num_interop_threads() + torch.get_num_threads())) // 2)
torch.set_num_threads((threads // 2))
torch.set_num_threads(threads)
