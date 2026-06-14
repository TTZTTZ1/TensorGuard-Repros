import sys
import torch

print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)

device = sys.argv[1] if len(sys.argv) > 1 else "cuda:0"
print("device:", device)

lstm = torch.nn.LSTM(10, 20, batch_first=True, num_layers=1, device=device)

print("before bidirectional:", lstm.bidirectional)
print("flat_weights:", len(lstm._flat_weights))

lstm.bidirectional = True

print("after bidirectional:", lstm.bidirectional)
print("flat_weights:", len(lstm._flat_weights))

lstm.flatten_parameters()
print("flatten ok")
