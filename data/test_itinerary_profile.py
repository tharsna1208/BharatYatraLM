from data.tourist_profile import TouristProfile

from data.itinerary_engine import (
    ItineraryEngine
)


engine = ItineraryEngine()


trip_days_list = [
    2,
    3,
    5
]


for trip_days in trip_days_list:

    profile = TouristProfile(

        travel_style="relaxing",

        traveler_type="couple",

        interests=[
            "beaches",
            "nature"
        ],

        budget=10000,

        trip_days=trip_days,

        crowd_preference="fewer crowds"
    )


    result = engine.get_itinerary(

        destination_name="Goa",

        trip_days=profile.trip_days,

        interests=profile.interests,

        traveler_type=profile.traveler_type
    )


    print(
        "\n" + "=" * 60
    )

    print(
        "Trip duration:",
        trip_days,
        "days"
    )

    print(
        "Status:",
        result["status"]
    )

    print(
        "Destination:",
        result["destination"]
    )

    print(
        "Traveler type:",
        profile.traveler_type
    )

    print(
        "Matching interests:",
        ", ".join(
            result["matching_interests"]
        )
    )

    print(
        "\nPersonalized itinerary:"
    )


    for item in result["days"]:

        print(
            f"\n{item['day']}"
        )

        print(
            f"Score: {item['score']}"
        )

        print(
            f"Reason: {item['reason']}"
        )