import torch
import torch.nn as nn


class TokenEmbedding(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size,
            embedding_dim
        )

    def forward(self, token_ids):
        return self.embedding(token_ids)


class PositionalEmbedding(nn.Module):
    def __init__(self, max_sequence_length, embedding_dim):
        super().__init__()

        self.position_embedding = nn.Embedding(
            max_sequence_length,
            embedding_dim
        )

    def forward(self, token_ids):
        sequence_length = token_ids.size(1)

        positions = torch.arange(
            sequence_length,
            device=token_ids.device
        )

        return self.position_embedding(positions)