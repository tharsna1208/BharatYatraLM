import math

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from data.tourism_dataset import TourismDataset
from models.bharatyatralm import BharatYatraLM


device = torch.device("cpu")


dataset = TourismDataset(
    "data/tourism_corpus.txt",
    "tokenizer/vocab_v2.json",
    context_length=128
)


dataloader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=False
)


vocab_size = len(
    dataset.tokenizer.token_to_id
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
        "models/bharatyatralm_v2.pth",
        map_location="cpu"
    )
)


model = model.to(device)

model.eval()


loss_function = nn.CrossEntropyLoss()


total_loss = 0


with torch.no_grad():

    for input_tokens, target_tokens in dataloader:

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


average_loss = (
    total_loss / len(dataloader)
)


perplexity = math.exp(
    average_loss
)


print("Evaluation Results")
print("------------------")

print(
    "Vocabulary size:",
    vocab_size
)

print(
    "Evaluation sequences:",
    len(dataset)
)

print(
    f"Average Loss: {average_loss:.4f}"
)

print(
    f"Perplexity: {perplexity:.4f}"
)