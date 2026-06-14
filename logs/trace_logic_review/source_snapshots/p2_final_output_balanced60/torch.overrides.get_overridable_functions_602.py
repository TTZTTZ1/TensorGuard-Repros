torch.set_default_tensor_type(torch.FloatTensor)
torch.default_dtype = torch.float32
torch.Tensor = (lambda x: torch.tensor(x))
torch.overrides.default_float_dtype = torch.float64
torch.overrides.default_dtype = float
torch.overrides.use_jit = False
torch.overrides.custom_type_deserializer = (lambda x: 0)
torch.overrides.custom_type_serializer = (lambda x: x)
torch.overrides.remove_unwanted_function = (lambda x: x)
torch.autograd.Function = (lambda x: torch.tensor(x))
x = torch.ones(10, requires_grad=True)
y = torch.rand(10, requires_grad=True)
z = (x + y)
result = torch.sum(z)
result = torch.overrides.get_overridable_functions()
for fn in result:
    print(fn)