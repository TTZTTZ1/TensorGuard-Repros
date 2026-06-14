
embed_dim = 512
num_heads = 8
seq_len = 64
query = torch.FloatTensor(4, seq_len, embed_dim)
key = query.clone()
value = query.clone()
(attn_output, attn_output_weights) = torch.nn.MultiheadAttention(embed_dim, num_heads)(query, key, value)
