from rag.recommendation_engine import (
    TourismRecommendationEngine
)


engine = TourismRecommendationEngine()


test_cases = [
    {
        "preferences": "peaceful beach couple",
        "budget": 10000,
        "trip_days": 3
    },
    {
        "preferences": "mountains adventure trekking",
        "budget": 15000,
        "trip_days": 7
    },
    {
        "preferences": "heritage culture history",
        "budget": 8000,
        "trip_days": 3
    }
]


for test in test_cases:

    print("\n" + "=" * 70)

    print(
        "\nPreferences:",
        test["preferences"]
    )

    print(
        "Budget:",
        test["budget"]
    )

    print(
        "Trip days:",
        test["trip_days"]
    )

    recommendations = engine.recommend(
        preferences=test["preferences"],
        budget=test["budget"],
        trip_days=test["trip_days"],
        top_k=5
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
            f"   Safety: "
            f"{item['safety_rating']:.1f}"
        )

        print(
            f"   Ideal days: "
            f"{item['ideal_trip_days']:.1f}"
        )

        print(
            f"   Why: "
            f"{item['explanation']}"
        )

        