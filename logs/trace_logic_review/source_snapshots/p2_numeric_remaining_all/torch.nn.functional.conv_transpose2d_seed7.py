input = torch.randn(1, 64, 56, 56)
weight = torch.randn(64, 128, 3, 3)
bias = torch.randn(128)
output = torch.nn.functional.conv_transpose2d(input, weight, bias=bias, stride=2, padding=1, output_padding=1, groups=1, dilation=1)