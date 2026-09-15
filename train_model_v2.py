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
    shuffle=True
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


model = model.to(device)


loss_function = nn.CrossEntropyLoss()


optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.0003
)


epochs = 3


for epoch in range(epochs):

    model.train()

    total_loss = 0

    for input_tokens, target_tokens in dataloader:

        input_tokens = input_tokens.to(device)
        target_tokens = target_tokens.to(device)

        optimizer.zero_grad()

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

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    average_loss = (
        total_loss / len(dataloader)
    )

    print(
        f"Epoch {epoch + 1}/{epochs} "
        f"- Average Loss: {average_loss:.4f}"
    )


torch.save(
    model.state_dict(),
    "models/bharatyatralm_v2.pth"
)


print("Model saved.")