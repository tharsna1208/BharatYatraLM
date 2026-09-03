import torch
from embeddings import TokenEmbedding, PositionalEmbedding


vocab_size = 1000
embedding_dim = 128
max_sequence_length = 128

token_embedding = TokenEmbedding(
    vocab_size,
    embedding_dim
)

position_embedding = PositionalEmbedding(
    max_sequence_length,
    embedding_dim
)

token_ids = torch.tensor([
    [10, 25, 100, 500]
])

token_vectors = token_embedding(token_ids)
position_vectors = position_embedding(token_ids)

combined_embeddings = token_vectors + position_vectors

print("Token embedding shape:", token_vectors.shape)
print("Position embedding shape:", position_vectors.shape)
print("Combined embedding shape:", combined_embeddings.shape)