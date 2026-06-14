
input_data = torch.randn(10, 3, 3, 64, 64)
batch_norm = torch.nn.BatchNorm3d(input_data.size(1))
batch_norm.running_mean.fill_(0.0)
batch_norm.running_var.fill_(1.0)
inputs = torch.Tensor(input_data.size()).fill_(0.1).unsqueeze_(1)
output = batch_norm(input_data)
output = output.view(output.size(0), (- 1))
