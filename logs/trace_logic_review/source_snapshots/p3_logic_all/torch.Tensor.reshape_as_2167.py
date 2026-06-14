
tensor_2 = torch.rand(2, 3)
tensor_2 = tensor_2.to('cpu')
tensor_1 = torch.Tensor(torch.Size([2, 3]))
tensor_2 = tensor_2.to('cpu')
torch.Tensor.reshape_as(tensor_1, tensor_2)
