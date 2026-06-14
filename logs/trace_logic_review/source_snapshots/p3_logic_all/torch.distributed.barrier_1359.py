
device = torch.device('cpu')
torch.set_num_threads(torch.get_num_threads())
torch.set_num_threads(20)
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = True
if (not torch.distributed.is_initialized()):
    torch.distributed.init_process_group(backend='nccl', init_method='tcp://127.0.0.1:23456', world_size=1, rank=0)
tensor = torch.ones(10)
tensor1 = torch.Tensor(range(10))
tensor2 = torch.Tensor(range(10, 20))
tensor3 = torch.Tensor(range(20, 30))
tensors = torch.stack([tensor1, tensor2, tensor3])
tensors = (tensors / 2)
torch.distributed.barrier()
torch.distributed.destroy_process_group()
