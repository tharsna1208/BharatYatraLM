import json


with open(
    "data/india_tourism_dataset.json",
    "r",
    encoding="utf-8"
) as file:

    destinations = json.load(
        file
    )


goa = next(
    destination
    for destination in destinations
    if destination[
        "destination_name"
    ] == "Goa"
)


print(
    "\nDestination:",
    goa["destination_name"]
)

print(
    "\nSuggested itinerary:"
)

print(
    goa["suggested_itinerary"]
)


print(
    "\nPrimary attractions:"
)

print(
    goa["primary_attractions"]
)


print(
    "\nActivities:"
)

print(
    goa["activities_available"]
)


print(
    "\nUnique experiences:"
)

print(
    goa["unique_experiences"]
)


print(
    "\nIdeal for:"
)

print(
    goa["ideal_for"]
)


print(
    "\nWhy it is suitable:"
)

print(
    goa["ideal_for_why"]
)