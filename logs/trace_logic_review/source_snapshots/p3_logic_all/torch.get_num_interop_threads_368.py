
threads = ((torch.get_num_interop_threads() + torch.get_num_threads()) // 2)
if (threads % 2):
    threads -= 1
torch.set_num_threads(threads)
