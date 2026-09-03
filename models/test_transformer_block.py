import torch
from transformer_block import TransformerBlock


embedding_dim = 128
num_heads = 4
feed_forward_dim = 512

block = TransformerBlock(
    embedding_dim,
    num_heads,
    feed_forward_dim
)

x = torch.randn(
    1,
    4,
    embedding_dim
)

output = block(x)

print("Input shape:", x.shape)
print("Output shape:", output.shape)