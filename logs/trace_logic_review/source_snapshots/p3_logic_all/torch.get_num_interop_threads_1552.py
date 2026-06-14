
threads = ((torch.get_num_interop_threads() + torch.get_num_threads()) // 2)
torch.set_num_threads(1)
torch.set_num_threads(64)
torch.set_num_threads(threads)
