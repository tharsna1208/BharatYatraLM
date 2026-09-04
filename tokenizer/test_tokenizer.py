from .tokenizer import SimpleTokenizer


text = "Goa is beautiful. Goa has beaches."

tokenizer = SimpleTokenizer(text)

sentence = "Goa has beautiful beaches."

token_ids = tokenizer.encode(
    sentence,
    max_length=8
)

print("Vocabulary:", tokenizer.token_to_id)
print("Token IDs:", token_ids)
print("Sequence length:", len(token_ids))
print("Decoded:", tokenizer.decode(token_ids))


import torch

from models.embeddings import TokenEmbedding


token_ids_tensor = torch.tensor([token_ids])

embedding = TokenEmbedding(
    vocab_size=len(tokenizer.token_to_id),
    embedding_dim=128
)

embedded_tokens = embedding(token_ids_tensor)

print("Token IDs shape:", token_ids_tensor.shape)
print("Embedding shape:", embedded_tokens.shape)


from models.embeddings import PositionalEmbedding


position_embedding = PositionalEmbedding(
    max_sequence_length=8,
    embedding_dim=128
)

position_vectors = position_embedding(token_ids_tensor)

combined_embeddings = embedded_tokens + position_vectors

print("Position embedding shape:", position_vectors.shape)
print("Combined embedding shape:", combined_embeddings.shape)


from models.transformer_block import TransformerBlock


transformer = TransformerBlock(
    embedding_dim=128,
    num_heads=4,
    feed_forward_dim=512
)

transformer_output = transformer(
    combined_embeddings
)

print("Transformer output shape:", transformer_output.shape)

tokenizer.save("tokenizer/vocab.json")

print("Vocabulary saved.")