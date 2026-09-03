import torch
from multi_head_attention import MultiHeadSelfAttention


embedding_dim = 128
num_heads = 4

attention = MultiHeadSelfAttention(
    embedding_dim,
    num_heads
)

x = torch.randn(
    1,
    4,
    embedding_dim
)

output = attention(x)

print("Input shape:", x.shape)
print("Output shape:", output.shape)