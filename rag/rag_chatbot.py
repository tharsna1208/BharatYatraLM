import json

from rag.documents import load_tourism_documents
from rag.semantic_retriever import SemanticTourismRetriever
from rag.answer_builder import build_answer


class RAGChatbot:

    def __init__(
        self,
        dataset_path="data/india_tourism_dataset.json"
    ):

        with open(
            dataset_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.destinations = json.load(
                file
            )

        self.documents = load_tourism_documents(
            dataset_path
        )

        self.retriever = SemanticTourismRetriever(
            self.documents
        )


    def find_destination(
        self,
        destination_name
    ):

        destination_name = (
            destination_name.lower()
        )

        for destination in self.destinations:

            name = destination.get(
                "destination_name",
                ""
            ).lower()

            if name == destination_name:
                return destination

        return None


    def answer(
        self,
        query
    ):

        retrieved_documents = (
            self.retriever.search(
                query,
                top_k=3
            )
        )

        if not retrieved_documents:

            return {
                "query": query,
                "destination": None,
                "similarity_score": 0.0,
                "answer": (
                    "I could not find relevant "
                    "tourism information."
                )
            }

        best_result = retrieved_documents[0]

        destination = self.find_destination(
            best_result[
                "destination_name"
            ]
        )

        if destination is None:

            return {
                "query": query,
                "destination":
                    best_result[
                        "destination_name"
                    ],
                "similarity_score":
                    best_result[
                        "similarity_score"
                    ],
                "answer": (
                    "I found a relevant destination "
                    "but could not retrieve its "
                    "structured information."
                )
            }

        answer = build_answer(
            query,
            destination
        )

        return {
            "query": query,
            "destination":
                best_result[
                    "destination_name"
                ],
            "similarity_score":
                best_result[
                    "similarity_score"
                ],
            "answer": answer
        }