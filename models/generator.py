import torch


class TextGenerator:

    def __init__(
        self,
        model,
        tokenizer,
        temperature=0.7,
        top_k=10,
        max_new_tokens=40
    ):

        self.model = model
        self.tokenizer = tokenizer

        self.temperature = temperature
        self.top_k = top_k
        self.max_new_tokens = max_new_tokens


    def generate(self, prompt):

        token_ids = self.tokenizer.encode(
            prompt
        )

        prompt_length = len(
            token_ids
        )

        self.model.eval()

        for _ in range(
            self.max_new_tokens
        ):

            input_tokens = torch.tensor(
                [token_ids[-128:]],
                dtype=torch.long
            )

            with torch.no_grad():

                logits = self.model(
                    input_tokens
                )

            last_logits = logits[
                0,
                -1
            ]

            scaled_logits = (
                last_logits
                / self.temperature
            )

            top_k_values, top_k_indices = torch.topk(
                scaled_logits,
                min(
                    self.top_k,
                    scaled_logits.size(-1)
                )
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

        generated_token_ids = token_ids[
            prompt_length:
        ]

        generated_text = self.tokenizer.decode(
            generated_token_ids
        )

        return generated_text.strip()