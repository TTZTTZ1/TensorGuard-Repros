
input_data = torch.randn(10, 3, 3, 64, 64)
batch_norm = torch.nn.BatchNorm3d(input_data.size(1))
input_data.uniform_((- 4), 4)
inputs = torch.Tensor(input_data.size()).fill_(0.1).unsqueeze_(1)
output = batch_norm(input_data)
output = inputs.mul(output)
output = torch.sign(output)
