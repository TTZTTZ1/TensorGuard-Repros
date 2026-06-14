
sequences = [torch.tensor([1, 2]), torch.tensor([3, 4, 5])]
sorted_sequences = sorted(sequences, key=len, reverse=True)
packed_sequences = torch.nn.utils.rnn.pack_sequence(sorted_sequences)
unpacked_sequences = packed_sequences[0]
packed = torch.nn.utils.rnn.pad_packed_sequence(packed_sequences, batch_first=True)
inputs = torch.zeros(6, 2)
unpacked_sequences = packed[0]
input_seq = packed_sequences[0][0]
inputs_len = unpacked_sequences.size(1)
