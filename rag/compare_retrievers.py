from rag.documents import load_tourism_documents
from rag.retriever import TourismRetriever
from rag.semantic_retriever import SemanticTourismRetriever


documents = load_tourism_documents(
    "data/india_tourism_dataset.json"
)


tfidf_retriever = TourismRetriever(
    documents
)


semantic_retriever = SemanticTourismRetriever(
    documents
)


queries = [
    "I want a relaxing coastal trip with fewer crowds",
    "I want a place for mountains and adventure",
    "I want a romantic trip with beautiful scenery"
]


for query in queries:

    print("\n" + "=" * 70)
    print("QUERY:")
    print(query)

    print("\nTF-IDF RESULTS")
    print("-" * 30)

    tfidf_results = tfidf_retriever.search(
        query,
        top_k=3
    )

    for result in tfidf_results:

        print(
            f"{result['destination_name']} "
            f"-> "
            f"{result['similarity_score']:.4f}"
        )

    print("\nSEMANTIC RESULTS")
    print("-" * 30)

    semantic_results = semantic_retriever.search(
        query,
        top_k=3
    )

    for result in semantic_results:

        print(
            f"{result['destination_name']} "
            f"-> "
            f"{result['similarity_score']:.4f}"
        )