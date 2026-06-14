
tensor_1 = torch.Tensor(torch.Size([2, 3])).to('cpu')
tensor_2 = torch.Tensor(torch.Size([2, 3]))
tensor_2 = tensor_2.to('cpu')
input_tensor = torch.tensor([[1, 2, 3], [4, 5, 6]])
torch.Tensor.reshape_as(tensor_2, tensor_1).copy_(input_tensor)
