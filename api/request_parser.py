import re


class TourismRequestParser:

    def __init__(self, destinations):

        self.destinations = destinations

        self.traveler_types = {
            "couple": "couple",
            "solo": "solo",
            "family": "family_with_kids",
            "kids": "family_with_kids",
            "children": "family_with_kids",
            "elderly": "family_with_elderly",
            "seniors": "family_with_elderly",
            "friends": "friends"
        }

        self.interest_keywords = {
            "beaches": [
                "beach",
                "beaches",
                "coastal",
                "sea"
            ],
            "nature": [
                "nature",
                "waterfalls",
                "waterfall",
                "forest",
                "forests",
                "wildlife",
                "lakes"
            ],
            "adventure": [
                "adventure",
                "trekking",
                "trek",
                "hiking",
                "rafting",
                "camping"
            ],
            "culture": [
                "culture",
                "heritage",
                "historical",
                "history",
                "temples",
                "temple",
                "churches",
                "church"
            ],
            "food": [
                "food",
                "cuisine",
                "restaurants",
                "restaurant",
                "street food"
            ],
            "nightlife": [
                "nightlife",
                "night life",
                "parties",
                "party",
                "clubs",
                "club"
            ],
            "shopping": [
                "shopping",
                "markets",
                "market",
                "shopping places"
            ],
            "peaceful": [
                "peaceful",
                "quiet",
                "calm",
                "relaxing",
                "relaxed"
            ]
        }

        self.number_words = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10
        }


    def extract_destination(self, text):

        text_lower = text.lower()

        for destination in self.destinations:

            name = destination.get(
                "destination_name",
                ""
            )

            if name.lower() in text_lower:
                return name

        return None


    def extract_trip_days(self, text):

        text_lower = text.lower()

        numeric_patterns = [
            r"\b(\d+)\s*day\b",
            r"\b(\d+)\s*days\b",
            r"\bfor\s+(\d+)\b",
            r"\b(\d+)\s*night\b",
            r"\b(\d+)\s*nights\b"
        ]

        for pattern in numeric_patterns:

            match = re.search(
                pattern,
                text_lower
            )

            if match:
                return int(match.group(1))


        word_pattern = (
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten)"
            r"\s*(?:day|days|night|nights)\b"
        )

        match = re.search(
            word_pattern,
            text_lower
        )

        if match:

            return self.number_words[
                match.group(1)
            ]


        return None


    def extract_traveler_type(self, text):

        text_lower = text.lower()

        for keyword, traveler_type in self.traveler_types.items():

            if re.search(
                rf"\b{re.escape(keyword)}\b",
                text_lower
            ):
                return traveler_type

        return None


    def extract_interests(self, text):

        text_lower = text.lower()

        interests = []

        for interest, keywords in self.interest_keywords.items():

            for keyword in keywords:

                if keyword in text_lower:

                    interests.append(interest)

                    break

        return interests


    def parse(self, text, intent):

        return {
            "intent": intent,
            "destination": self.extract_destination(text),
            "trip_days": self.extract_trip_days(text),
            "traveler_type": self.extract_traveler_type(text),
            "interests": self.extract_interests(text),
            "message": text
        }