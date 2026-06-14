
input = torch.randn(1, 16, 32, 32)
weight = torch.randn(16, 16, 1, 1)
output = torch.nn.functional.conv_transpose2d(input, weight)
