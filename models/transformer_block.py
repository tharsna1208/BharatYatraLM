import torch.nn as nn
from .multi_head_attention import MultiHeadSelfAttention
from .feed_forward import FeedForward


class TransformerBlock(nn.Module):
    def __init__(
        self,
        embedding_dim,
        num_heads,
        feed_forward_dim
    ):
        super().__init__()

        self.layer_norm_1 = nn.LayerNorm(
            embedding_dim
        )

        self.attention = MultiHeadSelfAttention(
            embedding_dim,
            num_heads
        )

        self.layer_norm_2 = nn.LayerNorm(
            embedding_dim
        )

        self.feed_forward = FeedForward(
            embedding_dim,
            feed_forward_dim
        )

    def forward(self, x):
        attention_output = self.attention(
            self.layer_norm_1(x)
        )

        x = x + attention_output

        feed_forward_output = self.feed_forward(
            self.layer_norm_2(x)
        )

        x = x + feed_forward_output

        return x