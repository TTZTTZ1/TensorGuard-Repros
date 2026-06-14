
tensor = torch.zeros(100, 100)
(tensor, idx) = tensor.sort(dim=0)
val = 4.0
torch.nn.init.constant_(tensor, val)
with torch.no_grad():
    val1 = torch.sum(tensor)
