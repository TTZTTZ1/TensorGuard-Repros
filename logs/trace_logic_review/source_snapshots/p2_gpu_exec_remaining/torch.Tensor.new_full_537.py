
_input_tensor = torch.randn(4, 4)
_output_tensor = torch.Tensor.new_full(_input_tensor, size=(4, 4), fill_value=2.0, dtype=torch.float64)
_loss = torch.nn.MSELoss(reduction='mean')
_loss.forward(_input_tensor, _output_tensor)
