from data.geospatial_engine import (
    GeospatialEngine
)


engine = GeospatialEngine()


nearest = engine.find_nearest(
    destination_name="Jaipur",
    top_k=5
)


print(
    "\n5 nearest destinations to Jaipur:"
)


for position, destination in enumerate(
    nearest,
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