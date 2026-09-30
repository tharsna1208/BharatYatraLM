import re

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TourismRecommendationEngine:

    def __init__(
        self,
        features_path="notebooks/features.csv"
    ):

        self.data = pd.read_csv(
            features_path
        )

        self.data[
            "destination_text"
        ] = self.data[
            "destination_text"
        ].fillna("")

        self.tourism_expansions = {
            "peaceful": [
                "peaceful",
                "quiet",
                "calm",
                "relaxing",
                "relaxed",
                "serene",
                "tranquil",
                "slow travel",
                "less crowded",
                "fewer crowds",
                "offbeat"
            ],
            "beach": [
                "beach",
                "beaches",
                "coastal",
                "coast",
                "sea",
                "shore",
                "seaside",
                "ocean"
            ],
            "nature": [
                "nature",
                "natural",
                "forest",
                "forests",
                "waterfall",
                "waterfalls",
                "wildlife",
                "lake",
                "lakes",
                "mountains",
                "valley",
                "greenery"
            ],
            "adventure": [
                "adventure",
                "trekking",
                "trek",
                "hiking",
                "rafting",
                "camping",
                "climbing",
                "sports",
                "outdoor"
            ],
            "culture": [
                "culture",
                "cultural",
                "heritage",
                "historical",
                "history",
                "temple",
                "temples",
                "church",
                "churches",
                "monastery",
                "traditions"
            ],
            "food": [
                "food",
                "cuisine",
                "restaurant",
                "restaurants",
                "street food",
                "local food",
                "dishes",
                "cafes"
            ],
            "nightlife": [
                "nightlife",
                "night life",
                "party",
                "parties",
                "clubs",
                "bars",
                "entertainment"
            ],
            "shopping": [
                "shopping",
                "markets",
                "market",
                "bazaars",
                "handicrafts",
                "souvenirs"
            ],
            "family": [
                "family",
                "families",
                "kids",
                "children",
                "elderly",
                "safe",
                "relaxed"
            ],
            "romantic": [
                "romantic",
                "couple",
                "couples",
                "honeymoon",
                "sunset",
                "romantic sunsets"
            ],
            "mountain": [
                "mountain",
                "mountains",
                "hill",
                "hills",
                "hill station",
                "valley",
                "himalayan"
            ],
            "spiritual": [
                "spiritual",
                "religious",
                "pilgrimage",
                "temple",
                "temples",
                "ashram",
                "monastery",
                "meditation",
                "yoga"
            ]
        }

        self.destination_text = (
            self.data[
                "destination_text"
            ].astype(str)
        )

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.destination_vectors = (
            self.vectorizer.fit_transform(
                self.destination_text
            )
        )

    def expand_preferences(
        self,
        preferences
    ):

        text = preferences.lower()

        expanded_terms = [
            text
        ]

        for category, terms in (
            self.tourism_expansions.items()
        ):

            category_found = False

            for term in terms:

                pattern = (
                    r"\b"
                    + re.escape(term)
                    + r"\b"
                )

                if re.search(
                    pattern,
                    text
                ):
                    category_found = True
                    break

            if category_found:

                expanded_terms.extend(
                    terms
                )

        return " ".join(
            expanded_terms
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
            / max(
                budget,
                1
            )
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

        if semantic_score >= 0.05:

            reasons.append(
                "it is a strong match for your travel preferences"
            )

        elif semantic_score >= 0.03:

            reasons.append(
                "it is a good match for your travel preferences"
            )

        else:

            reasons.append(
                "it somewhat matches your travel preferences"
            )

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

        expanded_preferences = (
            self.expand_preferences(
                preferences
            )
        )

        query_vector = (
            self.vectorizer.transform(
                [expanded_preferences]
            )
        )

        similarity_scores = (
            cosine_similarity(
                query_vector,
                self.destination_vectors
            )[0]
        )

        recommendations = []

        seen_destinations = set()

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

            if destination_name in (
                seen_destinations
            ):
                continue

            semantic_score = float(
                similarity_scores[index]
            )

            if semantic_score < 0.02:
                continue

            budget_score = (
                self.calculate_budget_score(
                    row,
                    budget
                )
            )

            duration_score = (
                self.calculate_duration_score(
                    row,
                    trip_days
                )
            )

            final_score = (
                0.60 * semantic_score
                + 0.25 * budget_score
                + 0.15 * duration_score
            )

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

            if len(recommendations) >= top_k:
                break

        recommendations.sort(
            key=lambda item:
                item["final_score"],
            reverse=True
        )

        return recommendations[
            :top_k
        ]