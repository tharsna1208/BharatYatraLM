import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class TourismRecommendationEngine:

    def __init__(
        self,
        features_path="notebooks/features.csv",
        model_name="all-MiniLM-L6-v2"
    ):

        self.data = pd.read_csv(
            features_path
        )

        self.data[
            "destination_text"
        ] = self.data[
            "destination_text"
        ].fillna("")

        self.model = SentenceTransformer(
            model_name
        )

        self.destination_embeddings = (
            self.model.encode(
                self.data[
                    "destination_text"
                ].tolist(),
                convert_to_numpy=True
            )
        )


    def calculate_budget_score(
        self,
        row,
        budget
    ):

        if budget is None:
            return 1.0

        minimum = float(
            row["budget_min"]
        )

        maximum = float(
            row["budget_max"]
        )

        if minimum <= budget <= maximum:
            return 1.0

        if budget < minimum:

            difference = (
                minimum - budget
            )

        else:

            difference = (
                budget - maximum
            )

        score = 1.0 - (
            difference
            / max(budget, 1)
        )

        return max(
            0.0,
            score
        )


    def calculate_duration_score(
        self,
        row,
        trip_days
    ):

        if trip_days is None:
            return 1.0

        ideal_days = float(
            row["ideal_trip_days"]
        )

        difference = abs(
            trip_days - ideal_days
        )

        score = 1.0 - (
            difference
            / max(
                ideal_days,
                trip_days,
                1
            )
        )

        return max(
            0.0,
            score
        )


    def create_explanation(
        self,
        row,
        semantic_score,
        budget_score,
        duration_score,
        budget,
        trip_days
    ):

        reasons = []


        # Semantic match
        if semantic_score >= 0.45:

            reasons.append(
                "it is a strong match for your travel preferences"
            )

        elif semantic_score >= 0.30:

            reasons.append(
                "it is a good match for your travel preferences"
            )

        else:

            reasons.append(
                "it somewhat matches your travel preferences"
            )


        # Budget
        if budget is not None:

            if budget_score >= 0.9:

                reasons.append(
                    "it fits your budget well"
                )

            elif budget_score >= 0.6:

                reasons.append(
                    "it is reasonably close to your budget"
                )

            else:

                reasons.append(
                    "it may require a higher budget"
                )


        # Trip duration
        if trip_days is not None:

            if duration_score >= 0.9:

                reasons.append(
                    "it matches your trip duration well"
                )

            elif duration_score >= 0.6:

                reasons.append(
                    "it is reasonably close to your trip duration"
                )

            else:

                reasons.append(
                    "it may need a different trip duration"
                )


        explanation = (
            "This destination is recommended because "
            + "; ".join(reasons)
            + "."
        )

        return explanation


    def recommend(
        self,
        preferences,
        budget=None,
        trip_days=None,
        top_k=5
    ):

        # Convert user preferences into an embedding
        query_embedding = self.model.encode(
            [preferences],
            convert_to_numpy=True
        )


        # Calculate semantic similarity
        similarity_scores = (
            cosine_similarity(
                query_embedding,
                self.destination_embeddings
            )[0]
        )


        recommendations = []

        seen_destinations = set()


        # Highest similarity first
        ranked_indices = (
            similarity_scores.argsort()[::-1]
        )


        for index in ranked_indices:

            row = self.data.iloc[
                index
            ]


            destination_name = (
                row[
                    "destination_name"
                ]
            )


            # Avoid duplicate destination names
            if destination_name in (
                seen_destinations
            ):
                continue


            semantic_score = float(
                similarity_scores[index]
            )


            # Ignore very weak semantic matches
            if semantic_score < 0.20:
                continue


            # Calculate budget compatibility
            budget_score = (
                self.calculate_budget_score(
                    row,
                    budget
                )
            )


            # Calculate trip-duration compatibility
            duration_score = (
                self.calculate_duration_score(
                    row,
                    trip_days
                )
            )


            # Hybrid recommendation score
            final_score = (
                0.60 * semantic_score
                + 0.25 * budget_score
                + 0.15 * duration_score
            )


            # Generate explanation
            explanation = (
                self.create_explanation(
                    row,
                    semantic_score,
                    budget_score,
                    duration_score,
                    budget,
                    trip_days
                )
            )


            recommendations.append({

                "destination_name":
                    destination_name,

                "similarity_score":
                    semantic_score,

                "budget_score":
                    budget_score,

                "duration_score":
                    duration_score,

                "final_score":
                    final_score,

                "popularity_score":
                    float(
                        row[
                            "popularity_score"
                        ]
                    ),

                "safety_rating":
                    float(
                        row[
                            "safety_rating"
                        ]
                    ),

                "ideal_trip_days":
                    float(
                        row[
                            "ideal_trip_days"
                        ]
                    ),

                "explanation":
                    explanation
            })


            seen_destinations.add(
                destination_name
            )


            # Stop after collecting enough
            # unique destinations
            if len(recommendations) >= top_k:
                break


        # Sort by final hybrid score
        recommendations.sort(
            key=lambda item:
                item["final_score"],
            reverse=True
        )


        return recommendations[
            :top_k
        ]