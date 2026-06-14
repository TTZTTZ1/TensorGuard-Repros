
num_threads = int(torch.get_num_threads())
(torch.set_num_threads(1) if (num_threads == (- 1)) else num_threads)
