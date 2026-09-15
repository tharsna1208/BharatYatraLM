from tokenizer.tokenizer import SimpleTokenizer


with open(
    "data/tourism_corpus.txt",
    "r",
    encoding="utf-8"
) as file:
    text = file.read()


tokenizer = SimpleTokenizer(text)


tokenizer.save(
    "tokenizer/vocab_v2.json"
)


print(
    "Vocabulary size:",
    len(tokenizer.token_to_id)
)

print(
    "Vocabulary saved to: tokenizer/vocab_v2.json"
)