import re


def normalize(text):

    text = str(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def format_list(value):

    if isinstance(value, list):

        items = [
            normalize(item)
            for item in value
            if str(item).strip()
        ]

        return ", ".join(items)

    return normalize(value)


def get_field(
    document,
    field_name
):

    return document.get(
        field_name,
        ""
    )


def detect_question_type(query):

    query = query.lower()

    if (
        "best time" in query
        or "when should" in query
        or "when is" in query
        or "season" in query
    ):
        return "best_time"

    if (
        "attraction" in query
        or "places to visit" in query
        or "what to see" in query
        or "sightseeing" in query
    ):
        return "attractions"

    if (
        "activity" in query
        or "things to do" in query
        or "what can i do" in query
    ):
        return "activities"

    if (
        "food" in query
        or "eat" in query
        or "cuisine" in query
        or "dish" in query
    ):
        return "food"

    if (
        "safe" in query
        or "safety" in query
    ):
        return "safety"

    if (
        "who should" in query
        or "ideal for" in query
        or "suitable for" in query
    ):
        return "ideal_for"

    if (
        "how many days" in query
        or "how long" in query
        or "itinerary" in query
    ):
        return "itinerary"

    if (
        "what is" in query
        or "tell me about" in query
        or "about" in query
    ):
        return "overview"

    return "overview"


def build_answer(
    query,
    document
):

    destination_name = normalize(
        document.get(
            "destination_name",
            ""
        )
    )

    question_type = detect_question_type(
        query
    )

    if question_type == "overview":

        state = normalize(
            get_field(
                document,
                "state"
            )
        )

        region = normalize(
            get_field(
                document,
                "region"
            )
        )

        return (
            f"{destination_name} is a tourist "
            f"destination in {state}, "
            f"in the {region} region."
        )

    if question_type == "attractions":

        attractions = format_list(
            get_field(
                document,
                "primary_attractions"
            )
        )

        return (
            f"The main attractions in "
            f"{destination_name} include "
            f"{attractions}."
        )

    if question_type == "activities":

        activities = format_list(
            get_field(
                document,
                "activities_available"
            )
        )

        return (
            f"Activities you can enjoy in "
            f"{destination_name} include "
            f"{activities}."
        )

    if question_type == "best_time":

        seasons = format_list(
            get_field(
                document,
                "best_seasons"
            )
        )

        return (
            f"The best time to visit "
            f"{destination_name} is "
            f"{seasons}."
        )

    if question_type == "food":

        cuisine = format_list(
            get_field(
                document,
                "local_cuisine_must_try"
            )
        )

        return (
            f"Local cuisine to try in "
            f"{destination_name} includes "
            f"{cuisine}."
        )

    if question_type == "safety":

        safety = normalize(
            get_field(
                document,
                "safety_notes"
            )
        )

        return (
            f"Safety information for "
            f"{destination_name}: "
            f"{safety}"
        )

    if question_type == "ideal_for":

        ideal_for = format_list(
            get_field(
                document,
                "ideal_for"
            )
        )

        return (
            f"{destination_name} is ideal for "
            f"{ideal_for}."
        )

    if question_type == "itinerary":

        itinerary = normalize(
            get_field(
                document,
                "suggested_itinerary"
            )
        )

        return (
            f"A suggested itinerary for "
            f"{destination_name} is: "
            f"{itinerary}"
        )

    return (
        f"{destination_name} is a tourist "
        f"destination in India."
    )