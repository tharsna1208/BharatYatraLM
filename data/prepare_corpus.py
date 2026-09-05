import json


def clean_text(text):
    text = str(text)

    replacements = {
        "â€“": "–",
        "â€”": "—",
        "â€™": "’",
        "â€œ": "“",
        "â€": "”",
        "â€¦": "…"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("..", ".")

    return text.strip()


input_file = "data/india_tourism_dataset.json"
output_file = "data/tourism_corpus.txt"


with open(input_file, "r", encoding="utf-8") as file:
    destinations = json.load(file)


corpus = []


for destination in destinations:

    name = destination.get("destination_name", "Unknown destination")
    state = destination.get("state", "")
    district = destination.get("district", "")
    region = destination.get("region", "")
    accessibility = destination.get("accessibility", "")
    road = destination.get("road_connectivity", "")

    attractions = destination.get("primary_attractions", [])
    activities = destination.get("activities_available", [])
    experiences = destination.get("unique_experiences", [])
    hidden_gems = destination.get("hidden_gems", [])

    best_seasons = destination.get("best_seasons", [])
    avoid_seasons = destination.get("avoid_seasons", [])

    ideal_for = destination.get("ideal_for", [])
    ideal_for_why = destination.get("ideal_for_why", "")

    min_days = destination.get("minimum_days", "")
    ideal_days = destination.get("ideal_days", "")
    max_days = destination.get("maximum_days", "")

    accommodation = destination.get("accommodation_types", [])
    food_scene = destination.get("food_scene", "")

    safety_rating = destination.get("safety_rating", "")
    safety_notes = destination.get("safety_notes", "")

    internet = destination.get("internet_connectivity", "")
    mobile = destination.get("mobile_network", "")
    atm = destination.get("atm_availability", "")

    languages = destination.get("language_spoken", [])
    culture = destination.get("local_culture", "")
    festivals = destination.get("festivals_events", [])
    customs = destination.get("local_customs", "")

    shopping = destination.get("shopping_highlights", [])
    cuisine = destination.get("local_cuisine_must_try", [])

    itinerary = destination.get("suggested_itinerary", "")
    considerations = destination.get("special_considerations", "")

    permits = destination.get("permits_required", "")
    permit_details = destination.get("permits_details", "")

    developments = destination.get("recent_developments", "")
    sustainability = destination.get("sustainability_notes", "")
    reviews = destination.get("user_reviews_summary", "")

    text = f"""
{name} is a tourist destination in {state}, {region}.
It is located in {district}.
The destination has {accessibility} accessibility.
Road connectivity is {road}.
The main attractions in {name} include {attractions}.
Activities available in {name} include {activities}.
Unique experiences include {experiences}.
Hidden gems include {hidden_gems}.
The best seasons to visit {name} are {best_seasons}.
The seasons to avoid are {avoid_seasons}.
{name} is ideal for {ideal_for}.
{name} is suitable for these travelers because {ideal_for_why}.
The minimum recommended trip duration is {min_days} days.
The ideal trip duration is {ideal_days} days.
The maximum recommended trip duration is {max_days} days.
Accommodation options include {accommodation}.
The food scene in {name} is {food_scene}.
The safety rating is {safety_rating}.
Safety information: {safety_notes}.
Internet connectivity is {internet}.
Mobile network availability is {mobile}.
ATM availability is {atm}.
Languages spoken include {languages}.
The local culture is {culture}.
Festivals and events include {festivals}.
Local customs include {customs}.
Shopping highlights include {shopping}.
Local cuisine to try includes {cuisine}.
A suggested itinerary for {name} is {itinerary}.
Special considerations include {considerations}.
Permits required: {permits}.
Permit details: {permit_details}.
Recent developments include {developments}.
Sustainability information: {sustainability}.
User review summary: {reviews}.
"""

    corpus.append(clean_text(text))


with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n\n".join(corpus))


print("Number of destinations:", len(destinations))
print("Number of training documents:", len(corpus))
print("Corpus saved to:", output_file)