import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


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


    def extract_location_matches(
        self,
        query
    ):

        query_lower = query.lower()

        matched_indices = set()

        for index, document in enumerate(
            self.documents
        ):

            location_fields = [
                document.get(
                    "destination_name",
                    ""
                ),
                document.get(
                    "state",
                    ""
                ),
                document.get(
                    "district",
                    ""
                ),
                document.get(
                    "region",
                    ""
                )
            ]

            for location in location_fields:

                if not location:
                    continue

                location_lower = (
                    str(location)
                    .lower()
                    .strip()
                )

                pattern = (
                    r"\b"
                    + re.escape(location_lower)
                    + r"\b"
                )

                if re.search(
                    pattern,
                    query_lower
                ):

                    matched_indices.add(
                        index
                    )

                    break

        return matched_indices


    def has_specific_location_query(
        self,
        query
    ):

        text = query.lower().strip()

        patterns = [
            r"\bin\s+([a-z][a-z\s&-]+)$",
            r"\bin\s+([a-z][a-z\s&-]+)\?",
            r"\babout\s+([a-z][a-z\s&-]+)$",
            r"\babout\s+([a-z][a-z\s&-]+)\?",
            r"\bfor\s+([a-z][a-z\s&-]+)$"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                location_phrase = (
                    match.group(1)
                    .strip()
                )

                location_phrase = re.sub(
                    r"\s+",
                    " ",
                    location_phrase
                )

                if location_phrase == "india":
                    return False

                if location_phrase in [
                    "the country",
                    "this country"
                ]:
                    return False

                return True

        return False


    def search(
        self,
        query,
        top_k=3
    ):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        location_matches = (
            self.extract_location_matches(
                query
            )
        )


        if location_matches:

            candidate_indices = list(
                location_matches
            )

        else:

            if self.has_specific_location_query(
                query
            ):

                return []

            candidate_indices = list(
                range(
                    len(self.documents)
                )
            )


        if not candidate_indices:

            return []


        candidate_embeddings = (
            self.document_embeddings[
                candidate_indices
            ]
        )


        similarity_scores = cosine_similarity(
            query_embedding,
            candidate_embeddings
        )[0]


        ranked_positions = (
            similarity_scores.argsort()[::-1]
        )


        results = []

        seen_destinations = set()


        for position in ranked_positions:

            original_index = (
                candidate_indices[position]
            )


            destination_name = (
                self.documents[
                    original_index
                ].get(
                    "destination_name",
                    ""
                )
            )


            if (
                destination_name
                in seen_destinations
            ):

                continue


            results.append({

                "destination_name":
                    destination_name,

                "text":
                    self.documents[
                        original_index
                    ].get(
                        "text",
                        ""
                    ),

                "similarity_score":
                    float(
                        similarity_scores[
                            position
                        ]
                    )
            })


            seen_destinations.add(
                destination_name
            )


            if len(results) == top_k:

                break


        return results