import json
import random
import re


INPUT_FILE = "data/india_tourism_dataset.json"
OUTPUT_FILE = "data/tourism_instructions.json"


def clean_text(text):

    text = str(text)

    # Remove web reference artifacts
    text = re.sub(
        r"\[web:\d+\]",
        "",
        text
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove repeated periods
    while ".." in text:
        text = text.replace(
            "..",
            "."
        )

    # Remove periods at the end of a value
    text = text.rstrip(".")

    return text.strip()


def clean_list(value):

    if not isinstance(value, list):
        return []

    return [
        clean_text(item)
        for item in value
        if str(item).strip()
    ]


def create_examples(destination):

    name = clean_text(
        destination.get(
            "destination_name",
            ""
        )
    )

    state = clean_text(
        destination.get(
            "state",
            ""
        )
    )

    region = clean_text(
        destination.get(
            "region",
            ""
        )
    )

    attractions = clean_list(
        destination.get(
            "primary_attractions",
            []
        )
    )

    activities = clean_list(
        destination.get(
            "activities_available",
            []
        )
    )

    ideal_for = clean_list(
        destination.get(
            "ideal_for",
            []
        )
    )

    best_seasons = clean_list(
        destination.get(
            "best_seasons",
            []
        )
    )

    cuisine = clean_list(
        destination.get(
            "local_cuisine_must_try",
            []
        )
    )

    itinerary = clean_text(
        destination.get(
            "suggested_itinerary",
            ""
        )
    )

    safety = clean_text(
        destination.get(
            "safety_notes",
            ""
        )
    )

    attractions_text = ", ".join(
        attractions
    )

    activities_text = ", ".join(
        activities
    )

    ideal_for_text = ", ".join(
        ideal_for
    )

    best_seasons_text = ", ".join(
        best_seasons
    )

    cuisine_text = ", ".join(
        cuisine
    )

    examples = []

    # 1. General information

    examples.append({
        "question": f"What is {name}?",
        "context": (
            f"{name} is located in {state}, "
            f"in the {region} region."
        ),
        "answer": (
            f"{name} is a tourist destination "
            f"located in {state}, in the "
            f"{region} region."
        )
    })

    # 2. Main attractions

    examples.append({
        "question": (
            f"What are the main attractions "
            f"in {name}?"
        ),
        "context": (
            f"The main attractions in {name} "
            f"include {attractions_text}."
        ),
        "answer": (
            f"The main attractions in {name} "
            f"include {attractions_text}."
        )
    })

    # 3. Activities

    examples.append({
        "question": (
            f"What activities can I do in {name}?"
        ),
        "context": (
            f"Activities available in {name} "
            f"include {activities_text}."
        ),
        "answer": (
            f"You can enjoy activities in {name} "
            f"such as {activities_text}."
        )
    })

    # 4. Suitable travelers

    examples.append({
        "question": (
            f"Who should visit {name}?"
        ),
        "context": (
            f"{name} is ideal for "
            f"{ideal_for_text}."
        ),
        "answer": (
            f"{name} is suitable for "
            f"{ideal_for_text}."
        )
    })

    # 5. Best time

    examples.append({
        "question": (
            f"When is the best time to visit {name}?"
        ),
        "context": (
            f"The best seasons for visiting {name} "
            f"are {best_seasons_text}."
        ),
        "answer": (
            f"The best time to visit {name} is "
            f"{best_seasons_text}."
        )
    })

    # 6. Food

    examples.append({
        "question": (
            f"What food should I try in {name}?"
        ),
        "context": (
            f"Local cuisine to try in {name} "
            f"includes {cuisine_text}."
        ),
        "answer": (
            f"When visiting {name}, you can try "
            f"local dishes such as "
            f"{cuisine_text}."
        )
    })

    # 7. Itinerary

    examples.append({
        "question": (
            f"How many days should I spend in {name}?"
        ),
        "context": (
            f"Suggested itinerary for {name}: "
            f"{itinerary}."
        ),
        "answer": (
            f"A suggested itinerary for {name} is "
            f"{itinerary}."
        )
    })

    # 8. Safety

    examples.append({
        "question": (
            f"What safety information should I know "
            f"about {name}?"
        ),
        "context": (
            f"Safety information for {name}: "
            f"{safety}."
        ),
        "answer": (
            f"For safety in {name}, "
            f"{safety}."
        )
    })

    return examples


# Load tourism dataset

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as file:

    destinations = json.load(file)


# Create instruction examples

all_examples = []

for destination in destinations:

    examples = create_examples(
        destination
    )

    all_examples.extend(
        examples
    )


# Shuffle examples

random.seed(42)

random.shuffle(
    all_examples
)


# Save instruction dataset

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        all_examples,
        file,
        indent=4,
        ensure_ascii=False
    )


print(
    "Instruction examples:",
    len(all_examples)
)

print(
    "Saved to:",
    OUTPUT_FILE
)