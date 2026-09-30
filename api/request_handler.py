import re
from api.router import detect_intent
from api.request_parser import TourismRequestParser

class TourismRequestHandler:
    def __init__(self, destinations):
        self.parser = TourismRequestParser(destinations)
        self.pending_recommendation = False

    def is_friend_trip_request(self, message):
        text = message.lower().strip()

        has_trip_intent = re.search(
            r"\btrip\b|\btravel\b|\bjourney\b|\bvacation\b",
            text
        )

        has_friend_intent = re.search(
            r"\bfriends?\b",
            text
        )

        return has_trip_intent and has_friend_intent

    def has_recommendation_preferences(self, message):
        interests = self.parser.extract_interests(message)
        trip_days = self.parser.extract_trip_days(message)

        return (
            len(interests) > 0
            or trip_days is not None
        )

    def process(self, message):
        if self.pending_recommendation:
            if self.has_recommendation_preferences(message):
                self.pending_recommendation = False

                parsed_request = self.parser.parse(
                    message,
                    "recommendation"
                )

                return parsed_request

            self.pending_recommendation = False

        intent = detect_intent(message)

        parsed_request = self.parser.parse(
            message,
            intent
        )

        if (
            intent == "itinerary"
            and parsed_request["destination"] is None
            and len(parsed_request["interests"]) > 0
        ):
            parsed_request["intent"] = "recommendation"

        if self.is_friend_trip_request(message):
            self.pending_recommendation = True

        return parsed_request