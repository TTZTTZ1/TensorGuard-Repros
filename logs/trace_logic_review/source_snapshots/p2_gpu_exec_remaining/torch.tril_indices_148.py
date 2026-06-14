
row = 5
col = 4
(row, col) = torch.LongTensor([row, col])
indices = torch.tril_indices(col, row)
