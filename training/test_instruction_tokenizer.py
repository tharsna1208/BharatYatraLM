from tokenizer.tokenizer import SimpleTokenizer


TOKENIZER_PATH = "tokenizer/vocab_instruction.json"


tokenizer = SimpleTokenizer.load(
    TOKENIZER_PATH
)


print(
    "Vocabulary size:",
    len(tokenizer.token_to_id)
)


test_text = (
    "Question: What is Goa? "
    "Tourism information: Goa has beaches. "
    "Answer:"
)


token_ids = tokenizer.encode(
    test_text
)


print(
    "\nOriginal text:"
)

print(
    test_text
)


print(
    "\nToken IDs:"
)

print(
    token_ids
)


print(
    "\nDecoded text:"
)

print(
    tokenizer.decode(
        token_ids
    )
)


print(
    "\nImportant tokens:"
)

for token in [
    "question",
    "tourism",
    "information",
    "answer"
]:

    token_id = tokenizer.token_to_id.get(
        token
    )

    print(
        token,
        "->",
        token_id
    )