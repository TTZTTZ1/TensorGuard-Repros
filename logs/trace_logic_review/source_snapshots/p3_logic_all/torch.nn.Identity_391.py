
input_data = torch.randn(10)
identity_output = torch.nn.Identity(dim=1)(torch.softmax(input_data, dim=(- 1)))
identity = (torch.sum(identity_output, dim=0) == 1)
