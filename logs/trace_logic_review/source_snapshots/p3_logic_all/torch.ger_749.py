
input = torch.arange((- 2.0), 2.0, 0.01)
vec = (input ** 2)
vec_exp = torch.exp((- vec))
vec_ger = torch.abs((vec - torch.ger(input, vec_exp)))
torch.ge(vec_ger, torch.ones_like(input, dtype=vec_ger.dtype, device=input.device)).all()
