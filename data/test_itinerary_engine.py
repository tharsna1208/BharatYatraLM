from data.itinerary_engine import (
    ItineraryEngine
)


engine = ItineraryEngine()


result = engine.get_itinerary(
    "Goa"
)


print(
    "\nStatus:",
    result["status"]
)

print(
    "Destination:",
    result["destination"]
)

print(
    "Minimum days:",
    result["minimum_days"]
)

print(
    "Ideal days:",
    result["ideal_days"]
)

print(
    "Maximum days:",
    result["maximum_days"]
)

print(
    "\nSuggested itinerary:"
)

print(
    result["suggested_itinerary"]
)