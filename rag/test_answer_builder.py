import json

from rag.answer_builder import build_answer


with open(
    "data/india_tourism_dataset.json",
    "r",
    encoding="utf-8"
) as file:

    destinations = json.load(file)


goa = None

for destination in destinations:

    if (
        destination.get(
            "destination_name",
            ""
        ).lower()
        == "goa"
    ):

        goa = destination
        break


if goa is None:

    print("Goa was not found.")

else:

    questions = [
        "What is Goa?",
        "What are the main attractions in Goa?",
        "What activities can I do in Goa?",
        "When is the best time to visit Goa?",
        "What food should I try in Goa?",
        "Who should visit Goa?",
        "What safety information should I know about Goa?",
        "How many days should I spend in Goa?"
    ]

    for question in questions:

        print("\n" + "=" * 60)

        print(
            "\nQuestion:"
        )

        print(
            question
        )

        print(
            "\nAnswer:"
        )

        print(
            build_answer(
                question,
                goa
            )
        )