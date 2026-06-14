
result = torch.arange(3, 7, dtype=torch.int32)
result = torch.combinations(result, 2)
result = torch.nonzero(result)
result = torch.zeros_like(result, dtype=result.dtype, device=result.device)
result = torch.max(result[0], result[1])
result = torch.randint(3, (4,), dtype=torch.int32, device=result.device)
result = torch.argsort(result)
