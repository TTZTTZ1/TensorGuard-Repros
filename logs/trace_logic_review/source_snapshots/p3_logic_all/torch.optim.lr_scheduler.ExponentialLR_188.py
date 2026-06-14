"""
{"exception": "RuntimeError", "msg": "Device index must not be negative"}
"""
X = torch.arange((- 10), 10, 0.01)
y = (X ** 2)
dataset = (X + y)
optimizer = torch.optim.SGD(torch.nn.Linear(10, 1).parameters(), lr=0.01)
scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, 0.95)
train = torch.randn(50, 1)
label = torch.arange(50, dtype=torch.float, device=train.get_device())