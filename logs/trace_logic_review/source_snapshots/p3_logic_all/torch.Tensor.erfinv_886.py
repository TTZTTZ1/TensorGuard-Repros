
input_value = np.arange((- 6), 6, 0.1)
result = torch.Tensor(input_value).erf()
output_value = torch.Tensor.erfinv(result)
