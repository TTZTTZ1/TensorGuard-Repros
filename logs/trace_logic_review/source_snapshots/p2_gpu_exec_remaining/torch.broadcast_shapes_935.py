
a = (torch.ones((1, 2, 3, 4)).type(torch.float32) / 3.0)
b = a
result = torch.broadcast_shapes(a.shape, b.shape, a.shape)
