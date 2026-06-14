
input_data = ((torch.randn(2, 3, 4) * 0.0) + 1.0)
torch.pinverse(input_data.unsqueeze(0))
