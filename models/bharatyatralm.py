import torch.nn as nn

from .embeddings import TokenEmbedding, PositionalEmbedding
from .transformer_block import TransformerBlock


class BharatYatraLM(nn.Module):
    def __init__(
        self,
        vocab_size,
        embedding_dim=128,
        num_heads=4,
        feed_forward_dim=512,
        num_layers=4,
        max_sequence_length=128
    ):
        super().__init__()

        self.token_embedding = TokenEmbedding(
            vocab_size,
            embedding_dim
        )

        self.position_embedding = PositionalEmbedding(
            max_sequence_length,
            embedding_dim
        )

        self.transformer_blocks = nn.ModuleList(
            [
                TransformerBlock(
                    embedding_dim,
                    num_heads,
                    feed_forward_dim
                )
                for _ in range(num_layers)
            ]
        )

        self.final_layer_norm = nn.LayerNorm(
            embedding_dim
        )

        self.output_projection = nn.Linear(
            embedding_dim,
            vocab_size
        )

    def forward(self, token_ids):

        x = self.token_embedding(token_ids)

        position_vectors = self.position_embedding(
            token_ids
        )

        x = x + position_vectors

        for block in self.transformer_blocks:
            x = block(x)

        x = self.final_layer_norm(x)

        logits = self.output_projection(x)

        return logits