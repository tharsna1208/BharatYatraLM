import torch

from .bharatyatralm import BharatYatraLM


vocab_size = 4192

model = BharatYatraLM(
    vocab_size=vocab_size,
    embedding_dim=128,
    num_heads=4,
    feed_forward_dim=512,
    num_layers=4,
    max_sequence_length=128
)


input_tokens = torch.randint(
    0,
    vocab_size,
    (4, 128)
)


logits = model(input_tokens)


print("Input shape:", input_tokens.shape)
print("Output shape:", logits.shape)