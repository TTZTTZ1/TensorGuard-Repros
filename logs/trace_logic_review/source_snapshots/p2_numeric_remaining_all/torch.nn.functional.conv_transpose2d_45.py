
input = torch.randn(1, 16, 56, 56)
weight = torch.randn(16, 1, 4, 4)
output = torch.nn.functional.conv_transpose2d(input, weight, padding=2, stride=2, groups=4)
