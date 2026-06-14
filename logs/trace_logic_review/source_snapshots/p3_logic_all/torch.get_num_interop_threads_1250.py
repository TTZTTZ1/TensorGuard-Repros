
threads = (((torch.get_num_interop_threads() + torch.get_num_threads()) // 2) // 4)
torch.set_num_threads((2 * threads))
