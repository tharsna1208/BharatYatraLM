from data.tourist_profile import TouristProfile

from data.geo_personalized_recommendation import (
    GeoPersonalizedRecommendation
)


profile = TouristProfile(

    travel_style="adventurous",

    traveler_type="solo",

    interests=[
        "mountains",
        "trekking",
        "adventure"
    ],

    budget=15000,

    trip_days=7,

    crowd_preference="moderate crowds"
)


engine = GeoPersonalizedRecommendation()


result = engine.recommend_nearby(

    profile=profile,

    location="Goa",

    radius_km=300,

    top_k=5
)


print(
    f"\nStatus: {result['status']}"
)

print(
    f"Location: {result['destination']}"
)

print(
    f"Radius: {result['radius_km']} km"
)


if result["status"] == "success":

    print(
        "\nPersonalized destinations near "
        f"{result['destination']}:"
    )


    for position, item in enumerate(
        result["results"],
        start=1
    ):

        print(
            f"\n{position}. "
            f"{item['destination_name']}"
        )

        print(
            f"   Distance: "
            f"{item['distance_km']:.2f} km"
        )

        print(
            f"   Preference match: "
            f"{item['similarity_score']:.4f}"
        )

        print(
            f"   Distance score: "
            f"{item['distance_score']:.4f}"
        )

        print(
            f"   Final score: "
            f"{item['final_score']:.4f}"
        )

        print(
            f"   Why: "
            f"{item['explanation']}"
        )


elif result["status"] == "destination_not_found":

    print(
        "\nThe location was not found "
        "in the tourism dataset."
    )


elif result["status"] == "no_destinations_found":

    print(
        "\nNo destinations were found "
        f"within {result['radius_km']} km."
    )