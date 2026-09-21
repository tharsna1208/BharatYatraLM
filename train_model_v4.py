import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from data.tourism_dataset import TourismDataset
from models.bharatyatralm import BharatYatraLM


device = torch.device("cpu")


train_dataset = TourismDataset(
    "data/tourism_train.txt",
    "tokenizer/vocab_v3.json",
    context_length=128
)


validation_dataset = TourismDataset(
    "data/tourism_validation.txt",
    "tokenizer/vocab_v3.json",
    context_length=128
)


train_dataloader = DataLoader(
    train_dataset,
    batch_size=4,
    shuffle=True
)


validation_dataloader = DataLoader(
    validation_dataset,
    batch_size=4,
    shuffle=False
)


vocab_size = len(
    train_dataset.tokenizer.token_to_id
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


epochs = 10


for epoch in range(epochs):

    model.train()

    total_train_loss = 0

    for input_tokens, target_tokens in train_dataloader:

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

        total_train_loss += loss.item()


    average_train_loss = (
        total_train_loss
        / len(train_dataloader)
    )


    model.eval()

    total_validation_loss = 0

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

            total_validation_loss += loss.item()


    average_validation_loss = (
        total_validation_loss
        / len(validation_dataloader)
    )


    print(
        f"Epoch {epoch + 1}/{epochs} "
        f"- Train Loss: {average_train_loss:.4f} "
        f"- Validation Loss: {average_validation_loss:.4f}"
    )


torch.save(
    model.state_dict(),
    "models/bharatyatralm_v4.pth"
)


print("Model saved.")