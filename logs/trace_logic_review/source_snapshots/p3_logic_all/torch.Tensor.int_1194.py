
torch.set_default_tensor_type('torch.DoubleTensor')
_default_dtype = torch.get_default_dtype()
torch.set_default_dtype(torch.float64)
_pytorch_version = torch.__version__
_pytorch_min_ver = torch.__version__.split('.')[0]
if (_pytorch_min_ver < '1.1.0'):
    raise RuntimeError('Pytorch < 1.0 required')
_input_tensor = 123
_input_tensor_bytes = (b'a' * 32)
_input_tensor = torch.Tensor(_input_tensor)
_input_tensor_int = torch.Tensor.int(_input_tensor)
_input_tensor_long = torch.Tensor.long(_input_tensor)
_input_tensor_short = torch.Tensor.short(_input_tensor)
_tensor_min = torch.min(_input_tensor)
_tensor_max = torch.max(_input_tensor)
_tensor_mean = torch.mean(_input_tensor)
_tensor_std = torch.std(_input_tensor)
torch.set_default_tensor_type(torch.FloatTensor)
_tensor_max = torch.max(_input_tensor)
