from data.geospatial_engine import (
    GeospatialEngine
)


engine = GeospatialEngine()


radius = 1


result = engine.find_nearby(
    destination_name="Goa",
    radius_km=radius,
    top_k=10
)


print(
    f"\nStatus: {result['status']}"
)

print(
    f"Destination: "
    f"{result['destination']}"
)


if result["status"] == "success":

    print(
        f"Radius: "
        f"{result['radius_km']} km"
    )

    print(
        f"\nDestinations within "
        f"{radius} km of "
        f"{result['destination']}:"
    )

    for position, destination in enumerate(
        result["results"],
        start=1
    ):

        print(
            f"\n{position}. "
            f"{destination['destination_name']}"
        )

        print(
            f"   Distance: "
            f"{destination['distance_km']:.2f} km"
        )


elif result["status"] == "destination_not_found":

    print(
        "\nDestination was not found "
        "in the tourism dataset."
    )


elif result["status"] == "no_destinations_found":

    print(
        f"\nNo destinations were found "
        f"within {result['radius_km']} km."
    )