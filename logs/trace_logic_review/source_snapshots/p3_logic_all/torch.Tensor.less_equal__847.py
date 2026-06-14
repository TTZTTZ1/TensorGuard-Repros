"""
{"exception": "AttributeError", "msg": "'bool' object has no attribute 'type'"}
"""

c = np.array([1.2, 0.3, 3.0])
torch.Tensor.less_equal_(torch.from_numpy(c), torch.from_numpy(c)).type()
