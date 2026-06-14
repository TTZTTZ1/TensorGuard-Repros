
input = torch.randn(1, 16, 32, 32)
weight = torch.randn(16, 1, 4, 4)
weight = torch.nn.functional.interpolate(weight, scale_factor=2, mode='nearest')
output = torch.nn.functional.conv_transpose2d(input, weight, padding=0, stride=2, groups=4)
