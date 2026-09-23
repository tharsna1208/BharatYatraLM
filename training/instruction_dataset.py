import json
import torch

from torch.utils.data import Dataset


class InstructionDataset(Dataset):

    def __init__(
        self,
        json_path,
        tokenizer,
        context_length=128
    ):

        with open(
            json_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.examples = json.load(file)

        self.tokenizer = tokenizer
        self.context_length = context_length
        self.samples = []

        self.prepare_samples()


    def prepare_samples(self):

        pad_id = self.tokenizer.token_to_id[
            "<PAD>"
        ]

        for example in self.examples:

            question = example[
                "question"
            ]

            context = example[
                "context"
            ]

            answer = example[
                "answer"
            ]

            prefix = (
                f"Question: {question} "
                f"Tourism information: {context} "
                f"Answer:"
            )

            full_text = (
                prefix
                + " "
                + answer
            )

            prefix_tokens = self.tokenizer.encode(
                prefix
            )

            full_tokens = self.tokenizer.encode(
                full_text
            )

            if len(full_tokens) < 2:
                continue

            full_tokens = full_tokens[
                :self.context_length
            ]

            if len(full_tokens) <= len(
                prefix_tokens
            ):
                continue

            input_ids = full_tokens[:-1]

            target_ids = full_tokens[1:]

            prefix_length = len(
                prefix_tokens
            )

            for i in range(
                len(target_ids)
            ):

                target_token_position = i + 1

                if target_token_position < prefix_length:

                    target_ids[i] = -100

            while len(input_ids) < (
                self.context_length - 1
            ):

                input_ids.append(
                    pad_id
                )

                target_ids.append(
                    -100
                )

            self.samples.append({
                "input_ids": input_ids,
                "target_ids": target_ids
            })


    def __len__(self):

        return len(
            self.samples
        )


    def __getitem__(self, index):

        sample = self.samples[
            index
        ]

        input_ids = torch.tensor(
            sample["input_ids"],
            dtype=torch.long
        )

        target_ids = torch.tensor(
            sample["target_ids"],
            dtype=torch.long
        )

        return (
            input_ids,
            target_ids
        )