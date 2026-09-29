import json
import re

from rag.documents import load_tourism_documents
from rag.semantic_retriever import SemanticTourismRetriever
from rag.answer_builder import build_answer


class RAGChatbot:

    def __init__(
        self,
        dataset_path="data/india_tourism_dataset.json"
    ):

        with open(
            dataset_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.destinations = json.load(
                file
            )

        self.documents = load_tourism_documents(
            dataset_path
        )

        self.retriever = SemanticTourismRetriever(
            self.documents
        )


    def find_destination(
        self,
        destination_name
    ):

        destination_name = (
            destination_name.lower()
        )

        for destination in self.destinations:

            name = destination.get(
                "destination_name",
                ""
            ).lower()

            if name == destination_name:
                return destination

        return None


    def conversation_response(
        self,
        query
    ):

        text = query.lower().strip()


        greeting_patterns = [
            r"^hi$",
            r"^hello$",
            r"^hey$",
            r"^hi there$",
            r"^hello there$",
            r"^hey there$",
            r"^good morning$",
            r"^good afternoon$",
            r"^good evening$"
        ]

        for pattern in greeting_patterns:

            if re.search(
                pattern,
                text
            ):

                return (
                    "Hi! I'm BharatYatraLM, "
                    "an AI tourism assistant for "
                    "exploring and planning journeys "
                    "across India. How can I help you today?"
                )


        identity_patterns = [
            r"\bwhat is your name\b",
            r"\bwhat's your name\b",
            r"\bwho are you\b",
            r"\bwho r u\b",
            r"\bwhat are you\b",
            r"\byour name\b"
        ]

        for pattern in identity_patterns:

            if re.search(
                pattern,
                text
            ):

                return (
                    "I'm BharatYatraLM, an AI tourism "
                    "assistant designed to help you "
                    "discover destinations, attractions, "
                    "nearby places, personalized recommendations, "
                    "and travel itineraries across India."
                )


        introduction_patterns = [
            r"\bintroduce yourself\b",
            r"\bintroduce urself\b",
            r"\btell me about yourself\b",
            r"\babout yourself\b",
            r"\bwho is bharatyatralm\b",
            r"\btell me about bharatyatralm\b"
        ]

        for pattern in introduction_patterns:

            if re.search(
                pattern,
                text
            ):

                return (
                    "I'm BharatYatraLM, an India-focused "
                    "AI tourism chatbot. I can help you "
                    "explore destinations, learn about "
                    "attractions, discover nearby places, "
                    "get personalized recommendations, "
                    "and create travel itineraries."
                )


        capability_patterns = [
            r"\bwhat can you do\b",
            r"\bwhat do you do\b",
            r"\bhow can you help me\b",
            r"\bwhat are your features\b",
            r"\bwhat can i ask you\b"
        ]

        for pattern in capability_patterns:

            if re.search(
                pattern,
                text
            ):

                return (
                    "I can help you explore India by "
                    "answering tourism questions, finding "
                    "nearby destinations, recommending places "
                    "based on your preferences, and creating "
                    "personalized trip itineraries."
                )


        thanks_patterns = [
            r"^thanks$",
            r"^thank you$",
            r"^thank u$",
            r"^thx$",
            r"^thanks a lot$"
        ]

        for pattern in thanks_patterns:

            if re.search(
                pattern,
                text
            ):

                return (
                    "You're welcome! "
                    "I'm happy to help with your India trip."
                )


        goodbye_patterns = [
            r"^bye$",
            r"^goodbye$",
            r"^see you$",
            r"^see you later$"
        ]

        for pattern in goodbye_patterns:

            if re.search(
                pattern,
                text
            ):

                return (
                    "Goodbye! Have a great journey "
                    "and enjoy exploring India."
                )


        friend_trip_patterns = [
            r"\btrip\b.*\bfriends\b",
            r"\bfriends\b.*\btrip\b",
            r"\btravel\b.*\bfriends\b",
            r"\bfriends\b.*\btravel\b",
            r"\bgo\b.*\btrip\b.*\bfriends\b",
            r"\bgo\b.*\btravel\b.*\bfriends\b"
        ]

        has_trip_intent = (
            re.search(
                r"\btrip\b|\btravel\b|\bjourney\b|\bvacation\b",
                text
            )
        )

        has_friend_intent = (
            re.search(
                r"\bfriends?\b",
                text
            )
        )

        has_specific_tourism_question = (
            re.search(
                r"\battractions?\b|\bplaces?\b|\bdestinations?\b|"
                r"\bhotels?\b|\bbeaches?\b|\btemples?\b|"
                r"\bactivities?\b|\bthings to do\b",
                text
            )
        )


        if (
            has_trip_intent
            and has_friend_intent
            and not has_specific_tourism_question
        ):

            return (
                "Absolutely! I can help you plan a trip "
                "with your friends. What kind of experience "
                "are you looking for — beaches, mountains, "
                "adventure, nature, food, nightlife, "
                "or something peaceful?"
            )


        return None


    def answer(
        self,
        query
    ):

        conversation_answer = (
            self.conversation_response(
                query
            )
        )


        if conversation_answer:

            return {
                "query": query,
                "destination": None,
                "similarity_score": 1.0,
                "answer": conversation_answer
            }


        retrieved_documents = (
            self.retriever.search(
                query,
                top_k=3
            )
        )


        if not retrieved_documents:

            return {
                "query": query,
                "destination": None,
                "similarity_score": 0.0,
                "answer": (
                    "I could not find relevant "
                    "tourism information."
                )
            }


        best_result = retrieved_documents[0]


        destination = self.find_destination(
            best_result[
                "destination_name"
            ]
        )


        if destination is None:

            return {
                "query": query,
                "destination":
                    best_result[
                        "destination_name"
                    ],
                "similarity_score":
                    best_result[
                        "similarity_score"
                    ],
                "answer": (
                    "I found a relevant destination "
                    "but could not retrieve its "
                    "structured information."
                )
            }


        answer = build_answer(
            query,
            destination
        )


        return {
            "query": query,
            "destination":
                best_result[
                    "destination_name"
                ],
            "similarity_score":
                best_result[
                    "similarity_score"
                ],
            "answer": answer
        }