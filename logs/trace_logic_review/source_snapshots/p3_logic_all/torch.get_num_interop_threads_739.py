
threads = ((torch.get_num_interop_threads() + torch.get_num_threads()) // 2)
for n in range(threads):
    torch.set_num_threads(1)
