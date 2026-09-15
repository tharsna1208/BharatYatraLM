import torch

from .bharatyatralm import BharatYatraLM
from tokenizer.tokenizer import SimpleTokenizer


tokenizer = SimpleTokenizer.load(
    "tokenizer/vocab_v2.json"
)


vocab_size = len(
    tokenizer.token_to_id
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


model.eval()


prompt = "Goa is"

token_ids = tokenizer.encode(
    prompt
)


temperature = 0.8
top_k = 20


for _ in range(20):

    input_tokens = torch.tensor(
        [token_ids[-128:]],
        dtype=torch.long
    )

    with torch.no_grad():
        logits = model(input_tokens)

    last_logits = logits[0, -1]

    scaled_logits = (
        last_logits / temperature
    )

    top_k_values, top_k_indices = torch.topk(
        scaled_logits,
        top_k
    )

    probabilities = torch.softmax(
        top_k_values,
        dim=-1
    )

    selected_index = torch.multinomial(
        probabilities,
        num_samples=1
    ).item()

    next_token_id = top_k_indices[
        selected_index
    ].item()

    token_ids.append(
        next_token_id
    )


generated_text = tokenizer.decode(
    token_ids
)


print("Generated text:")
print(generated_text)