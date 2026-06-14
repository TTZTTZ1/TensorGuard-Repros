
model = torch.nn.Linear(784, 500)
params = list(model.parameters())
flattened_params = torch.nn.utils.parameters_to_vector(params)
vectorized_params = torch.nn.Parameter(torch.Tensor(flattened_params.size()))
vectorized_params.requires_grad = False
