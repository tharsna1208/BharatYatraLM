import torch
import torch.nn as nn

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

target_tokens = torch.randint(
    0,
    vocab_size,
    (4, 128)
)


logits = model(input_tokens)


loss_function = nn.CrossEntropyLoss()


logits = logits.view(
    -1,
    vocab_size
)

target_tokens = target_tokens.view(-1)


loss = loss_function(
    logits,
    target_tokens
)


print("Logits shape:", logits.shape)
print("Target shape:", target_tokens.shape)
print("Loss:", loss.item())