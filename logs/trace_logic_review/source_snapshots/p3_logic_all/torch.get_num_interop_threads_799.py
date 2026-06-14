
threads = (((torch.get_num_interop_threads() + 1) * 2) // 2)
torch.set_num_threads((threads - ((torch.get_num_interop_threads() + torch.get_num_threads()) // 2)))
torch.set_num_threads((threads // 2))
torch.set_num_threads(threads)
