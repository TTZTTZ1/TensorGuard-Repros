
world_size = torch.distributed.get_world_size()
torch.distributed.broadcast_object_list(torch.Tensor(world_size))
