import math

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from data.tourism_dataset import TourismDataset
from models.bharatyatralm import BharatYatraLM


device = torch.device("cpu")


validation_dataset = TourismDataset(
    "data/tourism_validation.txt",
    "tokenizer/vocab_v3.json",
    context_length=128
)


validation_dataloader = DataLoader(
    validation_dataset,
    batch_size=4,
    shuffle=False
)


vocab_size = len(
    validation_dataset.tokenizer.token_to_id
)


model = BharatYatraLM(
    vocab_size=vocab_size,
    embedding_dim=128,
    num_heads=4,
    feed_forward_dim=512,
    num_layers=4,
    max_sequence_length=128
)


model.load_state_dict(
    torch.load(
        "models/bharatyatralm_v4.pth",
        map_location="cpu"
    )
)


model = model.to(device)

model.eval()


loss_function = nn.CrossEntropyLoss()


total_loss = 0


with torch.no_grad():

    for input_tokens, target_tokens in validation_dataloader:

        input_tokens = input_tokens.to(device)
        target_tokens = target_tokens.to(device)

        logits = model(input_tokens)

        logits = logits.view(
            -1,
            vocab_size
        )

        target_tokens = target_tokens.view(-1)

        loss = loss_function(
            logits,
            target_tokens
        )

        total_loss += loss.item()


average_validation_loss = (
    total_loss
    / len(validation_dataloader)
)


perplexity = math.exp(
    average_validation_loss
)


print("BharatYatraLM v4 Evaluation")
print("----------------------------")

print(
    "Vocabulary size:",
    vocab_size
)

print(
    "Validation sequences:",
    len(validation_dataset)
)

print(
    f"Validation Loss: "
    f"{average_validation_loss:.4f}"
)

print(
    f"Validation Perplexity: "
    f"{perplexity:.4f}"
)