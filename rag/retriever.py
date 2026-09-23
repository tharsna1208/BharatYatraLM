from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rag.documents import load_tourism_documents


class TourismRetriever:

    def __init__(self, documents):

        self.documents = documents

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.document_matrix = (
            self.vectorizer.fit_transform(
                [
                    document["text"]
                    for document in documents
                ]
            )
        )


    def search(
        self,
        query,
        top_k=3
    ):

        query_vector = (
            self.vectorizer.transform(
                [query]
            )
        )


        similarity_scores = (
            cosine_similarity(
                query_vector,
                self.document_matrix
            )[0]
        )


        ranked_indices = (
            similarity_scores.argsort()[::-1]
        )


        results = []


        for index in ranked_indices[:top_k]:

            results.append({

                "destination_name":
                    self.documents[index][
                        "destination_name"
                    ],

                "text":
                    self.documents[index][
                        "text"
                    ],

                "similarity_score":
                    float(
                        similarity_scores[index]
                    )
            })


        return results