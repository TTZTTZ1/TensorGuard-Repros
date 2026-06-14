
_output_tensor = torch.Tensor(size=(2, 4, 3))
_tril_tensor = torch.Tensor.tril(_output_tensor)
torch.testing.assert_allclose(_tril_tensor, torch.tril(_output_tensor))
