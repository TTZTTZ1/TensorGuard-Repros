
torch.set_num_threads(torch.get_num_threads())
torch.set_num_threads(8)
torch.set_num_threads(64)
if (not torch.distributed.is_initialized()):
    torch.distributed.init_process_group(backend='gloo', init_method='tcp://127.0.0.1:23456', world_size=1, rank=0)
torch.distributed.barrier()
torch.distributed.destroy_process_group()
