from data.geospatial_engine import (
    GeospatialEngine
)

from data.personalized_recommendation import (
    PersonalizedRecommendation
)


class GeoPersonalizedRecommendation:

    def __init__(self):

        self.geo_engine = (
            GeospatialEngine()
        )

        self.personalized_engine = (
            PersonalizedRecommendation()
        )


    def recommend_nearby(
        self,
        profile,
        location,
        radius_km=300,
        top_k=5
    ):

        nearby_result = (
            self.geo_engine.find_nearby(
                destination_name=location,
                radius_km=radius_km,
                top_k=20
            )
        )


        if nearby_result["status"] != "success":

            return {
                "status":
                    nearby_result["status"],

                "destination":
                    location,

                "radius_km":
                    radius_km,

                "results": []
            }


        nearby_destinations = (
            nearby_result["results"]
        )


        preference_text = (
            profile.build_preference_text()
        )


        recommendations = (
            self.personalized_engine.engine.recommend(
                preferences=preference_text,
                budget=profile.budget,
                trip_days=profile.trip_days,
                top_k=100
            )
        )


        recommendation_map = {

            item["destination_name"]:
                item

            for item in recommendations
        }


        combined_results = []


        for destination in nearby_destinations:

            name = (
                destination[
                    "destination_name"
                ]
            )


            if name not in recommendation_map:

                continue


            recommendation = (
                recommendation_map[name]
            )


            semantic_score = (
                recommendation[
                    "similarity_score"
                ]
            )


            distance = (
                destination[
                    "distance_km"
                ]
            )


            distance_score = max(
                0.0,
                1.0 - (
                    distance
                    / radius_km
                )
            )


            final_score = (
                0.75 * semantic_score
                + 0.25 * distance_score
            )


            combined_results.append({

                "destination_name":
                    name,

                "distance_km":
                    distance,

                "similarity_score":
                    semantic_score,

                "distance_score":
                    distance_score,

                "final_score":
                    final_score,

                "explanation":
                    recommendation[
                        "explanation"
                    ]
            })


        combined_results.sort(
            key=lambda item:
                item["final_score"],
            reverse=True
        )


        return {
            "status": "success",

            "destination":
                location,

            "radius_km":
                radius_km,

            "results":
                combined_results[
                    :top_k
                ]
        }