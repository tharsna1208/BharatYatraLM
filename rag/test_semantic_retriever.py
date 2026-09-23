from rag.documents import load_tourism_documents
from rag.semantic_retriever import SemanticTourismRetriever


documents = load_tourism_documents(
    "data/india_tourism_dataset.json"
)


retriever = SemanticTourismRetriever(
    documents
)


query = "I want a relaxing coastal trip with fewer crowds"


results = retriever.search(
    query,
    top_k=3
)


print("Query:")
print(query)


print("\nSemantic search results:")
print("------------------------")


for result in results:

    print(
        f"\nDestination: "
        f"{result['destination_name']}"
    )

    print(
        f"Similarity score: "
        f"{result['similarity_score']:.4f}"
    )

    print("\nRetrieved knowledge:")

    print(
        result["text"]
    )

    print(
        "\n" + "=" * 60
    )