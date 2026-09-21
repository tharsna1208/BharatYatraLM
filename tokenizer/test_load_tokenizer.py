from .tokenizer import SimpleTokenizer


tokenizer = SimpleTokenizer.load(
    "tokenizer/vocab.json"
)


print("Vocabulary size:", len(tokenizer.token_to_id))

sentence = "Goa is a beautiful tourist destination."

token_ids = tokenizer.encode(sentence)

print("Sentence:", sentence)
print("Token IDs:", token_ids)

decoded = tokenizer.decode(token_ids)

print("Decoded:", decoded)