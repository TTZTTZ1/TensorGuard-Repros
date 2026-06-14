
output_tensor = torch.Tensor.argsort(torch.argsort((torch.randn(3, 4, 5) * 100.0), dim=0)[0][0])
output_tensor.size()
