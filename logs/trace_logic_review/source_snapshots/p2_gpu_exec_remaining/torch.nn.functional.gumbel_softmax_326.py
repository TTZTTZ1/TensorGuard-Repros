
logits = torch.tensor([[0.5, (- 0.2), 0.8], [(- 0.1), 0.7, 0.4]])
tau = 1.0
logits = (logits + (torch.randn(*logits.shape) * tau))
output = torch.nn.functional.gumbel_softmax(logits, tau=1.0)
output = (output / torch.sum(output, dim=1, keepdim=True))
predict = torch.nn.functional.log_softmax(output, dim=(- 1))
predict = (predict / torch.sum(predict, dim=1, keepdim=True))
predict = predict.detach().numpy()
predict2 = predict
