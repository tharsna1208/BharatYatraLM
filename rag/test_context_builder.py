from rag.documents import load_tourism_documents
from rag.semantic_retriever import SemanticTourismRetriever
from rag.context_builder import build_context


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


prompt = build_context(
    query,
    results
)


print("Generated RAG Prompt:")
print("---------------------")
print(prompt)