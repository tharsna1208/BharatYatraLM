import json
import re


def clean_text(text):

    text = str(text)

    text = re.sub(
        r"\[web:\d+\]",
        "",
        text
    )

    text = text.replace(
        "reefsnear",
        "reefs near"
    )

    text = text.replace(
        "healthys",
        "healthy s"
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def format_list(value):

    if isinstance(value, list):

        text = ", ".join(
            str(item)
            for item in value
        )

        return clean_text(text)

    return clean_text(value)


def format_dict(value):

    if isinstance(value, dict):

        text = ". ".join(
            f"{key}: {val}"
            for key, val in value.items()
        )

        return clean_text(text)

    return clean_text(value)


def create_destination_document(
    destination
):

    name = destination.get(
        "destination_name",
        ""
    )

    state = destination.get(
        "state",
        ""
    )

    district = destination.get(
        "district",
        ""
    )

    region = destination.get(
        "region",
        ""
    )

    attractions = destination.get(
        "primary_attractions",
        []
    )

    activities = destination.get(
        "activities_available",
        []
    )

    experiences = destination.get(
        "unique_experiences",
        []
    )

    best_seasons = destination.get(
        "best_seasons",
        []
    )

    ideal_for = destination.get(
        "ideal_for",
        []
    )

    ideal_for_why = destination.get(
        "ideal_for_why",
        {}
    )

    itinerary = destination.get(
        "suggested_itinerary",
        ""
    )

    cuisine = destination.get(
        "local_cuisine_must_try",
        []
    )

    accommodation = destination.get(
        "accommodation_types",
        []
    )

    safety = destination.get(
        "safety_notes",
        ""
    )

    culture = destination.get(
        "local_culture",
        ""
    )

    document = f"""
Destination: {name}
State: {state}
District: {district}
Region: {region}

Main attractions: {format_list(attractions)}

Activities: {format_list(activities)}

Unique experiences: {format_list(experiences)}

Best seasons: {format_list(best_seasons)}

Ideal for: {format_list(ideal_for)}

Why it is suitable:
{format_dict(ideal_for_why)}

Suggested itinerary:
{clean_text(itinerary)}

Accommodation:
{format_list(accommodation)}

Local cuisine:
{format_list(cuisine)}

Local culture:
{clean_text(culture)}

Safety information:
{clean_text(safety)}
"""

    return clean_text(document)


def load_tourism_documents(
    file_path
):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        destinations = json.load(file)

    documents = []

    for destination in destinations:

        document = create_destination_document(
            destination
        )

        documents.append({
            "destination_name": destination.get(
                "destination_name",
                ""
            ),
            "text": document
        })

    return documents