import torch

from tokenizer.tokenizer import SimpleTokenizer
from models.bharatyatralm import BharatYatraLM


OLD_MODEL_PATH = "models/bharatyatralm_v4.pth"
OLD_TOKENIZER_PATH = "tokenizer/vocab_v3.json"
NEW_TOKENIZER_PATH = "tokenizer/vocab_instruction.json"
NEW_MODEL_PATH = "models/bharatyatralm_instruction_base.pth"


old_tokenizer = SimpleTokenizer.load(
    OLD_TOKENIZER_PATH
)

old_vocab_size = len(
    old_tokenizer.token_to_id
)


new_tokenizer = SimpleTokenizer.load(
    NEW_TOKENIZER_PATH
)

new_vocab_size = len(
    new_tokenizer.token_to_id
)


print(
    "Old vocabulary size:",
    old_vocab_size
)

print(
    "New vocabulary size:",
    new_vocab_size
)


old_model = BharatYatraLM(
    vocab_size=old_vocab_size
)


old_model.load_state_dict(
    torch.load(
        OLD_MODEL_PATH,
        map_location="cpu"
    )
)


new_model = BharatYatraLM(
    vocab_size=new_vocab_size
)


old_state = old_model.state_dict()

new_state = new_model.state_dict()


for name in new_state:

    if name not in old_state:
        continue

    old_tensor = old_state[name]

    new_tensor = new_state[name]

    if old_tensor.shape == new_tensor.shape:

        new_state[name] = old_tensor

    elif (
        len(old_tensor.shape) == 2
        and
        old_tensor.shape[1] == new_tensor.shape[1]
        and
        old_tensor.shape[0] < new_tensor.shape[0]
    ):

        new_tensor[:old_tensor.shape[0]] = (
            old_tensor
        )

        new_state[name] = new_tensor

    elif (
        len(old_tensor.shape) == 1
        and
        old_tensor.shape[0] < new_tensor.shape[0]
    ):

        new_tensor[:old_tensor.shape[0]] = (
            old_tensor
        )

        new_state[name] = new_tensor


new_model.load_state_dict(
    new_state
)


torch.save(
    new_model.state_dict(),
    NEW_MODEL_PATH
)


print(
    "\nExpanded model created successfully."
)

print(
    "Saved to:",
    NEW_MODEL_PATH
)

print(
    "New model vocabulary size:",
    new_vocab_size
)