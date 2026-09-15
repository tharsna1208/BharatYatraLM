import torch
from torch.utils.data import Dataset

from tokenizer.tokenizer import SimpleTokenizer


class TourismDataset(Dataset):

    def __init__(
        self,
        corpus_path,
        tokenizer_path,
        context_length=128
    ):

        with open(
            corpus_path,
            "r",
            encoding="utf-8"
        ) as file:
            text = file.read()

        self.tokenizer = SimpleTokenizer.load(
            tokenizer_path
        )

        self.tokens = self.tokenizer.encode(
            text
        )

        self.context_length = context_length

        self.num_sequences = (
            len(self.tokens) - 1
        ) // context_length

    def __len__(self):
        return self.num_sequences

    def __getitem__(self, index):

        start = index * self.context_length

        input_tokens = self.tokens[
            start:start + self.context_length
        ]

        target_tokens = self.tokens[
            start + 1:start + self.context_length + 1
        ]

        return (
            torch.tensor(
                input_tokens,
                dtype=torch.long
            ),
            torch.tensor(
                target_tokens,
                dtype=torch.long
            )
        )