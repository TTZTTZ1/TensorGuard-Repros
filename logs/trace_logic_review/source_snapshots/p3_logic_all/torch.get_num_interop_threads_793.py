
threads = ((torch.get_num_interop_threads() + torch.get_num_threads()) // 4)
torch.set_num_threads((threads // 4))
torch.set_num_threads(threads)
