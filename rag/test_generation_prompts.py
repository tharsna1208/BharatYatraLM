import torch

from tokenizer.tokenizer import SimpleTokenizer
from models.bharatyatralm import BharatYatraLM
from models.generator import TextGenerator


tokenizer = SimpleTokenizer.load(
    "tokenizer/vocab_v3.json"
)


model = BharatYatraLM(
    vocab_size=len(
        tokenizer.token_to_id
    )
)


model.load_state_dict(
    torch.load(
        "models/bharatyatralm_v4.pth",
        map_location="cpu"
    )
)


model.eval()


generator = TextGenerator(
    model,
    tokenizer,
    temperature=0.7,
    top_k=10,
    max_new_tokens=40
)


prompts = [
    "Goa is",
    "Question: What is Goa? Answer:",
    "Question: I want a beach trip. Tourism information: Goa has beaches and water sports. Answer:"
]


for prompt in prompts:

    print("\n" + "=" * 70)

    print("PROMPT:")
    print(prompt)

    print("\nGENERATED:")
    print(
        generator.generate(prompt)
    )