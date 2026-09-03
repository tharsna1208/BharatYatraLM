import torch
from feed_forward import FeedForward


embedding_dim = 128
hidden_dim = 512

feed_forward = FeedForward(
    embedding_dim,
    hidden_dim
)

x = torch.randn(
    1,
    4,
    embedding_dim
)

output = feed_forward(x)

print("Input shape:", x.shape)
print("Output shape:", output.shape)