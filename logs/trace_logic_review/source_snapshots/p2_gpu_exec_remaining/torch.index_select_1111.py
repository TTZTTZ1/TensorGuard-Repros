
input_tensor = torch.randn(3, 4, 3, 2)
input_tensor = input_tensor.to(torch.device('cpu'))
dim = 1
index = torch.tensor(torch.arange(input_tensor.size(0), device=input_tensor.device))
index = torch.cat(torch.meshgrid(index.view((- 1)), index.view((- 1))), dim=dim)
index = index.flatten()
result = torch.index_select(input_tensor, dim, index)
result = torch.tensor(result.cpu())
result = result.permute(1, 0, 2, 3)
result = result.numpy()
