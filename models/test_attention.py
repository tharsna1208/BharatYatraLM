import torch
from attention import SelfAttention


embedding_dim = 128

attention = SelfAttention(
    embedding_dim
)

x = torch.randn(
    1,
    4,
    embedding_dim
)

output = attention(x)

print("Input shape:", x.shape)
print("Output shape:", output.shape)