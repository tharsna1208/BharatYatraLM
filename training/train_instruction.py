import torch
from torch.utils.data import DataLoader

from tokenizer.tokenizer import SimpleTokenizer
from models.bharatyatralm import BharatYatraLM
from training.instruction_dataset import InstructionDataset


TOKENIZER_PATH = "tokenizer/vocab_instruction.json"
DATASET_PATH = "data/tourism_instructions.json"
MODEL_PATH = "models/bharatyatralm_instruction_base.pth"
OUTPUT_PATH = "models/bharatyatralm_instruction_v2.pth"

CONTEXT_LENGTH = 128
BATCH_SIZE = 4
EPOCHS = 3
LEARNING_RATE = 0.00005


device = torch.device(
    "cpu"
)


tokenizer = SimpleTokenizer.load(
    TOKENIZER_PATH
)


dataset = InstructionDataset(
    DATASET_PATH,
    tokenizer,
    context_length=CONTEXT_LENGTH
)


dataloader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)


model = BharatYatraLM(
    vocab_size=len(
        tokenizer.token_to_id
    )
)


model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)


model.to(device)


optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE
)


criterion = torch.nn.CrossEntropyLoss(
    ignore_index=-100
)


model.train()


for epoch in range(EPOCHS):

    total_loss = 0.0

    for input_ids, target_ids in dataloader:

        input_ids = input_ids.to(
            device
        )

        target_ids = target_ids.to(
            device
        )

        optimizer.zero_grad()

        logits = model(
            input_ids
        )

        loss = criterion(
            logits.reshape(
                -1,
                logits.size(-1)
            ),
            target_ids.reshape(
                -1
            )
        )

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0
        )

        optimizer.step()

        total_loss += loss.item()

    average_loss = (
        total_loss
        / len(dataloader)
    )

    print(
        f"Epoch {epoch + 1}/{EPOCHS} "
        f"Loss: {average_loss:.4f}"
    )


torch.save(
    model.state_dict(),
    OUTPUT_PATH
)


print(
    "\nInstruction training completed."
)

print(
    "Saved to:",
    OUTPUT_PATH
)