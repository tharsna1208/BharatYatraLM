def build_context(
    query,
    retrieved_documents,
    max_context_characters=700
):

    if not retrieved_documents:
        return (
            f"Question: {query}. "
            f"Tourism information: "
            f"No relevant information found. "
            f"Answer:"
        )

    document = retrieved_documents[0]

    destination_name = document[
        "destination_name"
    ]

    text = document[
        "text"
    ]

    text = text.replace(
        f"Destination: {destination_name}",
        "",
        1
    ).strip()

    text = text[:max_context_characters]

    last_sentence_end = max(
        text.rfind(". "),
        text.rfind(".")
    )

    if last_sentence_end > 100:
        text = text[
            :last_sentence_end + 1
        ]

    context = (
        f"Destination: "
        f"{destination_name}. "
        f"{text}"
    )

    prompt = (
        f"Question: {query}. "
        f"Tourism information: "
        f"{context} "
        f"Answer:"
    )

    return prompt