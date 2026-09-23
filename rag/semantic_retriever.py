from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from rag.documents import load_tourism_documents


class SemanticTourismRetriever:

    def __init__(
        self,
        documents,
        model_name="all-MiniLM-L6-v2"
    ):

        self.documents = documents

        self.model = SentenceTransformer(
            model_name
        )

        self.document_embeddings = (
            self.model.encode(
                [
                    document["text"]
                    for document in documents
                ],
                convert_to_numpy=True
            )
        )

    def search(
        self,
        query,
        top_k=3
    ):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        similarity_scores = cosine_similarity(
            query_embedding,
            self.document_embeddings
        )[0]

        ranked_indices = (
            similarity_scores.argsort()[::-1]
        )

        results = []

        seen_destinations = set()

        for index in ranked_indices:

            destination_name = self.documents[index][
                "destination_name"
            ]

            if destination_name in seen_destinations:
                continue

            results.append({

                "destination_name":
                    destination_name,

                "text":
                    self.documents[index][
                        "text"
                    ],

                "similarity_score":
                    float(
                        similarity_scores[index]
                    )
            })

            seen_destinations.add(
                destination_name
            )

            if len(results) == top_k:
                break

        return results