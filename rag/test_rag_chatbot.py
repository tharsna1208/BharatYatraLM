from rag.rag_chatbot import RAGChatbot


chatbot = RAGChatbot()


questions = [
    "What is Goa?",
    "What are the main attractions in Goa?",
    "When is the best time to visit Goa?",
    "What food should I try in Goa?",
    "Who should visit Goa?",
    "What safety information should I know about Goa?",
    "How many days should I spend in Goa?"
]


for question in questions:

    result = chatbot.answer(
        question
    )

    print("\n" + "=" * 60)

    print(
        "\nQuestion:"
    )

    print(
        question
    )

    print(
        "\nRetrieved destination:"
    )

    print(
        result["destination"]
    )

    print(
        "\nSimilarity score:"
    )

    print(
        result["similarity_score"]
    )

    print(
        "\nAnswer:"
    )

    print(
        result["answer"]
    )