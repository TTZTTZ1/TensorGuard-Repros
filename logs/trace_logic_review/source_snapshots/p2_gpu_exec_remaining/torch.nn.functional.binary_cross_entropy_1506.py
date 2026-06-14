
target = torch.ones(10, 100)
output = torch.sigmoid(torch.randn(10, 100))
output = torch.sigmoid(output)
loss = torch.sum((torch.nn.functional.binary_cross_entropy(output, target, reduction='mean') * ((output > 0.5) ** 2)))
loss.mean()
