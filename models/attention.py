import torch
import torch.nn as nn
import math


class SelfAttention(nn.Module):
    def __init__(self, embedding_dim):
        super().__init__()

        self.query = nn.Linear(embedding_dim, embedding_dim)
        self.key = nn.Linear(embedding_dim, embedding_dim)
        self.value = nn.Linear(embedding_dim, embedding_dim)

    def forward(self, x):
        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)

        scores = Q @ K.transpose(-2, -1)

        scores = scores / math.sqrt(Q.size(-1))

        mask = torch.tril(
            torch.ones(
                x.size(1),
                x.size(1),
                device=x.device
            )
        )

        scores = scores.masked_fill(
            mask == 0,
            float("-inf")
        )

        attention_weights = torch.softmax(
            scores,
            dim=-1
        )

        output = attention_weights @ V

        return output