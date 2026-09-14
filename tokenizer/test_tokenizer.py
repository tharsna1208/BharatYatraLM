from .tokenizer import SimpleTokenizer


with open(
    "data/tourism_corpus.txt",
    "r",
    encoding="utf-8"
) as file:
    text = file.read()


tokenizer = SimpleTokenizer(text)

print("Vocabulary size:", len(tokenizer.token_to_id))

sentence = "Goa is a beautiful tourist destination."

token_ids = tokenizer.encode(sentence)

print("Sentence:", sentence)
print("Token IDs:", token_ids)
print("Number of tokens:", len(token_ids))

decoded = tokenizer.decode(token_ids)

print("Decoded:", decoded)

tokenizer.save("tokenizer/vocab.json")

print("Vocabulary saved.")