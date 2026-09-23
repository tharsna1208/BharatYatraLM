import torch

from tokenizer.tokenizer import SimpleTokenizer
from models.bharatyatralm import BharatYatraLM
from models.generator import TextGenerator


TOKENIZER_PATH = "tokenizer/vocab_instruction.json"
MODEL_PATH = "models/bharatyatralm_instruction_v2.pth"


tokenizer = SimpleTokenizer.load(
    TOKENIZER_PATH
)


model = BharatYatraLM(
    vocab_size=len(
        tokenizer.token_to_id
    )
)


model.load_state_dict(
    torch.load(
        MODEL_PATH,
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
    (
        "Question: What is Goa? "
        "Tourism information: Goa is a coastal destination "
        "in India with beaches and water activities. "
        "Answer:"
    ),
    (
        "Question: What are the main attractions in Goa? "
        "Tourism information: Goa has beaches, forts, "
        "water sports and historic churches. "
        "Answer:"
    ),
    (
        "Question: When is the best time to visit Goa? "
        "Tourism information: The best season for Goa "
        "is from November to February. "
        "Answer:"
    )
]


for prompt in prompts:

    print("\n" + "=" * 60)

    print("\nPrompt:")
    print(prompt)

    print("\nGenerated:")
    print(
        generator.generate(
            prompt
        )
    )