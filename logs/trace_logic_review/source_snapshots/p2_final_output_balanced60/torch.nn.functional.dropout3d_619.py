
input_tensor = torch.randn(3, 4, 4, 5, 5).type(torch.FloatTensor)
output_tensor = torch.nn.functional.dropout(input_tensor, 0.5, False)
output = torch.nn.functional.dropout3d(output_tensor, 0.5)
output = torch.nn.functional.dropout3d(output, 0.5)
torch.allclose(output, output_tensor, atol=0.5, rtol=1e-05)
if True:
    torch.set_default_dtype(torch.float64)
