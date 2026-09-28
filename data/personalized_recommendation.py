from rag.recommendation_engine import (
    TourismRecommendationEngine
)


class PersonalizedRecommendation:

    def __init__(self):

        self.engine = (
            TourismRecommendationEngine()
        )


    def recommend_for_profile(
        self,
        profile,
        top_k=5
    ):

        preference_text = (
            profile.build_preference_text()
        )

        recommendations = (
            self.engine.recommend(
                preferences=preference_text,
                budget=profile.budget,
                trip_days=profile.trip_days,
                top_k=top_k
            )
        )

        return recommendations