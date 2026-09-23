import torch

from models.bharatyatralm import BharatYatraLM
from models.generator import TextGenerator
from tokenizer.tokenizer import SimpleTokenizer


tokenizer = SimpleTokenizer.load(
    "tokenizer/vocab_v3.json"
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
        "models/bharatyatralm_v4.pth",
        map_location="cpu"
    )
)


generator = TextGenerator(
    model=model,
    tokenizer=tokenizer,
    temperature=0.8,
    top_k=20,
    max_new_tokens=40
)


prompt = "Goa is"


generated_text = generator.generate(
    prompt
)


print("Generated text:")
print(generated_text)