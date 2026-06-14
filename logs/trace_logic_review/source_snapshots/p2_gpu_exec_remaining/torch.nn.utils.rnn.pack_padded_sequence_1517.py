
input_data = torch.autograd.Variable(torch.rand(4, 5, 6, 7))
lengths = [5, 4, 3, 2]
packed_seq = torch.nn.utils.rnn.pack_padded_sequence(input_data, lengths, batch_first=True)
(sequence, _) = torch.nn.utils.rnn.pad_packed_sequence(packed_seq, batch_first=True)
output_data = sequence.index_select(dim=1, index=torch.LongTensor([2, 3])).type_as(sequence)
(output_data.size() == torch.Size([5, 4, 6, 7]))
(torch.autograd.Variable(output_data) == output_data)
