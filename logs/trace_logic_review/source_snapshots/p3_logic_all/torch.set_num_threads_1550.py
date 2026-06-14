"""
{"exception": "RuntimeError", "msg": "set_num_threads expects an int, but got float"}
"""

num_threads = int(torch.get_num_threads())
torch.set_num_threads(max(1, (num_threads / 5)))
