
num_threads = int(torch.get_num_threads())
torch.set_num_threads((num_threads * 2))
