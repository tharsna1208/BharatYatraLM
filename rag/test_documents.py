from rag.documents import load_tourism_documents


documents = load_tourism_documents(
    "data/india_tourism_dataset.json"
)


print(
    "Number of documents:",
    len(documents)
)


print(
    "\nFirst destination:"
)


print(
    documents[0]["destination_name"]
)


print(
    "\nDocument:"
)


print(
    documents[0]["text"]
)