from tokenizer.tokenizer import SimpleTokenizer
from training.instruction_dataset import InstructionDataset


tokenizer = SimpleTokenizer.load(
    "tokenizer/vocab_instruction.json"
)


dataset = InstructionDataset(
    "data/tourism_instructions.json",
    tokenizer,
    context_length=128
)


print(
    "Number of samples:",
    len(dataset)
)


input_ids, target_ids = dataset[0]


print(
    "Input shape:",
    input_ids.shape
)


print(
    "Target shape:",
    target_ids.shape
)


print(
    "\nFirst input tokens:"
)

print(
    input_ids[:20].tolist()
)


print(
    "\nFirst target tokens:"
)

print(
    target_ids[:20].tolist()
)


valid_positions = [
    i
    for i, token_id in enumerate(
        target_ids.tolist()
    )
    if token_id != -100
]


print(
    "\nNumber of answer tokens:",
    len(valid_positions)
)


if valid_positions:

    first_answer_position = valid_positions[0]

    answer_token_ids = [
        token_id
        for token_id in target_ids.tolist()
        if token_id != -100
    ]

    print(
        "First answer position:",
        first_answer_position
    )

    print(
        "\nAnswer token IDs:"
    )

    print(
        answer_token_ids[:20]
    )

    print(
        "\nDecoded answer tokens:"
    )

    print(
        tokenizer.decode(
            answer_token_ids[:20]
        )
    )

else:

    print(
        "\nERROR: No answer tokens found."
    )