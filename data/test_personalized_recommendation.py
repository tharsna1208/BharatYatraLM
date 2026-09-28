from data.tourist_profile import TouristProfile

from data.personalized_recommendation import (
    PersonalizedRecommendation
)


personalized = (
    PersonalizedRecommendation()
)


profiles = [

    {
        "name": "Beach Couple",

        "profile": TouristProfile(
            travel_style="peaceful",
            traveler_type="couple",
            interests=[
                "beaches",
                "nature"
            ],
            budget=10000,
            trip_days=3,
            crowd_preference="fewer crowds"
        )
    },

    {
        "name": "Adventure Solo",

        "profile": TouristProfile(
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
    },

    {
        "name": "Heritage Family",

        "profile": TouristProfile(
            travel_style="cultural",
            traveler_type="family",
            interests=[
                "heritage",
                "history",
                "culture"
            ],
            budget=12000,
            trip_days=4,
            crowd_preference="moderate crowds"
        )
    }
]


for person in profiles:

    profile = person["profile"]

    print("\n" + "=" * 70)

    print(
        "PROFILE:",
        person["name"]
    )

    print("=" * 70)

    print(
        "\nPreferences:"
    )

    print(
        profile.build_preference_text()
    )

    print(
        "\nBudget:",
        profile.budget
    )

    print(
        "Trip days:",
        profile.trip_days
    )

    recommendations = (
        personalized.recommend_for_profile(
            profile,
            top_k=5
        )
    )

    print(
        "\nRecommendations:"
    )

    for position, item in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"\n{position}. "
            f"{item['destination_name']}"
        )

        print(
            f"   Similarity: "
            f"{item['similarity_score']:.4f}"
        )

        print(
            f"   Budget match: "
            f"{item['budget_score']:.4f}"
        )

        print(
            f"   Duration match: "
            f"{item['duration_score']:.4f}"
        )

        print(
            f"   Final score: "
            f"{item['final_score']:.4f}"
        )

        print(
            f"   Why: "
            f"{item['explanation']}"
        )