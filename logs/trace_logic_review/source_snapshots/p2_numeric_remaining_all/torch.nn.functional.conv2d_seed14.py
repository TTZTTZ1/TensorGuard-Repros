input = torch.randn(1, 16, 50, 50)
weight = torch.randn(32, 16, 5, 5)
bias = torch.randn(32)
output = torch.nn.functional.conv2d(input, weight, bias=bias, stride=1, padding=0, dilation=1, groups=1)