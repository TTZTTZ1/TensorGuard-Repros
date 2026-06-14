"""
{"exception": "AttributeError", "msg": "'Tensor' object has no attribute 'sparse_coo_tensor'"}
"""

indices = torch.tensor([[0, 1, 1], [2, 0, 2]])
values = torch.tensor([3.0, 4.0, 5.0])
size = torch.Size([3, 3])
sparse_tensor = torch.sparse_coo_tensor(torch.ones_like(indices), values, size)
sparse_tensor.dense = torch.randn(3)
sparse_tensor.indices = torch.arange(3)
sparse_tensor.values = torch.ones(3)
for _ in range(10):
    print(sparse_tensor.sparse_coo_tensor())
