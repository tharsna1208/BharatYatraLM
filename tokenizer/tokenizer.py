import re
import json


class SimpleTokenizer:
    def __init__(self, text):
        words = re.findall(r"\w+|[^\w\s]", text.lower())

        vocabulary = sorted(set(words))

        self.token_to_id = {
            "<PAD>": 0,
            "<UNK>": 1
        }

        for word in vocabulary:
            if word not in self.token_to_id:
                self.token_to_id[word] = len(self.token_to_id)

        self.id_to_token = {
            token_id: token
            for token, token_id in self.token_to_id.items()
        }

    def encode(self, text, max_length=None):
        words = re.findall(
            r"\w+|[^\w\s]",
            text.lower()
        )

        token_ids = [
            self.token_to_id.get(word, 1)
            for word in words
        ]

        if max_length is not None:
            token_ids = token_ids[:max_length]

            while len(token_ids) < max_length:
                token_ids.append(
                    self.token_to_id["<PAD>"]
                )

        return token_ids

    def decode(self, token_ids):
        return " ".join(
            self.id_to_token.get(
                token_id,
                "<UNK>"
            )
            for token_id in token_ids
        )

    def save(self, path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.token_to_id, file, indent=4)