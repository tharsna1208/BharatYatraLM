import json
import re


OLD_VOCAB_FILE = "tokenizer/vocab_v3.json"
INSTRUCTION_FILE = "data/tourism_instructions.json"
NEW_VOCAB_FILE = "tokenizer/vocab_instruction.json"


def tokenize_text(text):

    return re.findall(
        r"\w+|[^\w\s]",
        text.lower()
    )


# Load existing vocabulary

with open(
    OLD_VOCAB_FILE,
    "r",
    encoding="utf-8"
) as file:

    old_vocab = json.load(file)


# Load instruction dataset

with open(
    INSTRUCTION_FILE,
    "r",
    encoding="utf-8"
) as file:

    instruction_data = json.load(file)


# Copy existing vocabulary

new_vocab = dict(old_vocab)


# Add tokens from instruction dataset

for example in instruction_data:

    combined_text = (
        example.get("question", "")
        + " "
        + example.get("context", "")
        + " "
        + example.get("answer", "")
    )

    tokens = tokenize_text(
        combined_text
    )

    for token in tokens:

        if token not in new_vocab:

            new_vocab[token] = len(
                new_vocab
            )


# Explicitly add instruction control words

instruction_tokens = [
    "question",
    "tourism",
    "information",
    "answer"
]


for token in instruction_tokens:

    if token not in new_vocab:

        new_vocab[token] = len(
            new_vocab
        )


# Save vocabulary

with open(
    NEW_VOCAB_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        new_vocab,
        file,
        indent=4,
        ensure_ascii=False
    )


print(
    "Old vocabulary size:",
    len(old_vocab)
)

print(
    "New vocabulary size:",
    len(new_vocab)
)

print(
    "Added tokens:",
    len(new_vocab) - len(old_vocab)
)

print(
    "Saved to:",
    NEW_VOCAB_FILE
)


print(
    "\nInstruction tokens:"
)

for token in instruction_tokens:

    print(
        token,
        "->",
        new_vocab[token]
    )