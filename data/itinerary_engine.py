import json
import re


class ItineraryEngine:

    def __init__(
        self,
        dataset_path="data/india_tourism_dataset.json"
    ):

        with open(
            dataset_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.destinations = json.load(file)


    def find_destination(
        self,
        destination_name
    ):

        destination_name = destination_name.lower()

        for destination in self.destinations:

            name = destination.get(
                "destination_name",
                ""
            ).lower()

            if name == destination_name:
                return destination

        return None


    def parse_itinerary(
        self,
        itinerary
    ):

        if not itinerary:
            return []

        days = re.findall(
            r"Day\s+\d+:\s*.*?(?=;\s*Day\s+\d+:|$)",
            itinerary
        )

        return [
            day.strip()
            for day in days
        ]


    def normalize_to_list(
        self,
        value
    ):

        if isinstance(value, list):
            return value

        if isinstance(value, str):
            return [value]

        return []


    def extract_tourism_data(
        self,
        destination
    ):

        return {
            "primary_attractions":
                self.normalize_to_list(
                    destination.get(
                        "primary_attractions",
                        []
                    )
                ),

            "activities_available":
                self.normalize_to_list(
                    destination.get(
                        "activities_available",
                        []
                    )
                ),

            "unique_experiences":
                self.normalize_to_list(
                    destination.get(
                        "unique_experiences",
                        []
                    )
                ),

            "ideal_for":
                self.normalize_to_list(
                    destination.get(
                        "ideal_for",
                        []
                    )
                ),

            "ideal_for_why":
                destination.get(
                    "ideal_for_why",
                    {}
                )
        }


    def build_tourism_knowledge(
        self,
        tourism_data
    ):

        sections = []

        for item in tourism_data[
            "primary_attractions"
        ]:

            sections.append(str(item))

        for item in tourism_data[
            "activities_available"
        ]:

            sections.append(str(item))

        for item in tourism_data[
            "unique_experiences"
        ]:

            sections.append(str(item))

        for item in tourism_data[
            "ideal_for"
        ]:

            sections.append(str(item))

        return ", ".join(sections)


    def normalize_word(
        self,
        word
    ):

        word = word.lower().strip()

        if word.endswith("ies"):
            word = word[:-3] + "y"

        elif word.endswith("es"):
            word = word[:-2]

        elif word.endswith("s"):
            word = word[:-1]

        return word


    def normalize_interest(
        self,
        interest
    ):

        words = re.findall(
            r"[a-z]+",
            interest.lower()
        )

        return [
            self.normalize_word(word)
            for word in words
        ]


    def find_matching_interests(
        self,
        interests,
        tourism_knowledge
    ):

        knowledge = re.sub(
            r"[^a-z0-9\s]",
            " ",
            tourism_knowledge.lower()
        )

        knowledge_words = {
            self.normalize_word(word)
            for word in knowledge.split()
        }

        matching_interests = []

        for interest in interests:

            normalized_words = (
                self.normalize_interest(
                    interest
                )
            )

            for word in normalized_words:

                if word in knowledge_words:

                    matching_interests.append(
                        interest
                    )

                    break

        return matching_interests


    def match_traveler_type(
        self,
        traveler_type,
        tourism_data
    ):

        if not traveler_type:
            return False

        traveler_type = (
            traveler_type.lower()
            .replace("_", " ")
            .strip()
        )

        for ideal_type in tourism_data[
            "ideal_for"
        ]:

            normalized_type = (
                ideal_type.lower()
                .replace("_", " ")
                .strip()
            )

            if traveler_type == normalized_type:
                return True

        return False


    def get_traveler_type_reason(
        self,
        traveler_type,
        tourism_data
    ):

        if not traveler_type:
            return ""

        traveler_type = (
            traveler_type.lower()
            .replace("_", " ")
            .strip()
        )

        reasons = tourism_data[
            "ideal_for_why"
        ]

        if not isinstance(
            reasons,
            dict
        ):
            return ""

        for traveler, reason in reasons.items():

            normalized_traveler = (
                traveler.lower()
                .replace("_", " ")
                .strip()
            )

            if normalized_traveler == traveler_type:
                return str(reason)

        return ""


    def get_day_words(
        self,
        day
    ):

        normalized_day = re.sub(
            r"[^a-z0-9\s]",
            " ",
            day.lower()
        )

        return {
            self.normalize_word(word)
            for word in normalized_day.split()
        }


    def get_reason_words(
        self,
        traveler_reason
    ):

        if not traveler_reason:
            return set()

        reason_words = re.findall(
            r"[a-z]+",
            traveler_reason.lower()
        )

        return {
            self.normalize_word(word)
            for word in reason_words
            if len(
                self.normalize_word(word)
            ) >= 4
        }


    def calculate_day_score(
        self,
        day,
        interests,
        traveler_reason
    ):

        day_words = self.get_day_words(
            day
        )

        score = 0

        interest_matched = False

        for interest in interests:

            normalized_words = (
                self.normalize_interest(
                    interest
                )
            )

            for word in normalized_words:

                if word in day_words:

                    score += 2
                    interest_matched = True
                    break

        if traveler_reason:

            reason_words = (
                self.get_reason_words(
                    traveler_reason
                )
            )

            if (
                reason_words
                & day_words
            ):

                if not interest_matched:
                    score += 1

        return score


    def create_day_reason(
        self,
        day,
        interests,
        traveler_reason,
        score
    ):

        day_words = self.get_day_words(
            day
        )

        matched_interests = []

        for interest in interests:

            normalized_words = (
                self.normalize_interest(
                    interest
                )
            )

            for word in normalized_words:

                if word in day_words:

                    matched_interests.append(
                        interest
                    )

                    break

        traveler_match = False

        if traveler_reason:

            reason_words = (
                self.get_reason_words(
                    traveler_reason
                )
            )

            if reason_words & day_words:

                traveler_match = True

        if matched_interests and traveler_match:

            return (
                "Selected because it matches "
                "your interest in "
                + ", ".join(
                    matched_interests
                )
                + " and matches your "
                "traveler preferences."
            )

        if matched_interests:

            return (
                "Selected because it matches "
                "your interest in "
                + ", ".join(
                    matched_interests
                )
                + "."
            )

        if traveler_match:

            return (
                "Selected because it matches "
                "your traveler preferences."
            )

        if score == 0:

            return (
                "Included as part of the "
                "destination's itinerary."
            )

        return (
            "Selected based on your "
            "travel preferences."
        )


    def personalize_days(
        self,
        days,
        interests,
        traveler_reason=""
    ):

        if not days:
            return []

        scored_days = []

        for position, day in enumerate(days):

            score = (
                self.calculate_day_score(
                    day,
                    interests,
                    traveler_reason
                )
            )

            reason = (
                self.create_day_reason(
                    day,
                    interests,
                    traveler_reason,
                    score
                )
            )

            scored_days.append({
                "day": day,
                "score": score,
                "reason": reason,
                "original_position": position
            })

        scored_days.sort(
            key=lambda item: (
                -item["score"],
                item["original_position"]
            )
        )

        return scored_days


    def adapt_to_duration(
        self,
        days,
        trip_days
    ):

        if trip_days <= 0:
            return []

        if len(days) <= trip_days:

            days.sort(
                key=lambda item:
                    item["original_position"]
            )

            return [
                item
                for item in days
            ]

        selected_days = days[:trip_days]

        selected_days.sort(
            key=lambda item:
                item["original_position"]
        )

        return [
            item
            for item in selected_days
        ]


    def get_itinerary(
        self,
        destination_name,
        trip_days=None,
        interests=None,
        traveler_type=None
    ):

        destination = self.find_destination(
            destination_name
        )

        if destination is None:

            return {
                "status":
                    "destination_not_found",

                "destination":
                    destination_name,

                "days": []
            }

        itinerary = destination.get(
            "suggested_itinerary",
            ""
        )

        days = self.parse_itinerary(
            itinerary
        )

        tourism_data = (
            self.extract_tourism_data(
                destination
            )
        )

        tourism_knowledge = (
            self.build_tourism_knowledge(
                tourism_data
            )
        )

        matching_interests = []

        if interests:

            matching_interests = (
                self.find_matching_interests(
                    interests,
                    tourism_knowledge
                )
            )

        traveler_type_match = (
            self.match_traveler_type(
                traveler_type,
                tourism_data
            )
        )

        traveler_type_reason = (
            self.get_traveler_type_reason(
                traveler_type,
                tourism_data
            )
        )

        scored_days = (
            self.personalize_days(
                days,
                matching_interests,
                traveler_type_reason
            )
        )

        if trip_days is not None:

            selected_days = (
                self.adapt_to_duration(
                    scored_days,
                    trip_days
                )
            )

        else:

            scored_days.sort(
                key=lambda item:
                    item["original_position"]
            )

            selected_days = [
                item
                for item in scored_days
            ]

        return {

            "status":
                "success",

            "destination":
                destination[
                    "destination_name"
                ],

            "minimum_days":
                destination[
                    "minimum_days"
                ],

            "ideal_days":
                destination[
                    "ideal_days"
                ],

            "maximum_days":
                destination[
                    "maximum_days"
                ],

            "suggested_itinerary":
                itinerary,

            "tourism_data":
                tourism_data,

            "tourism_knowledge":
                tourism_knowledge,

            "matching_interests":
                matching_interests,

            "traveler_type_match":
                traveler_type_match,

            "traveler_type_reason":
                traveler_type_reason,

            "days":
                selected_days
        }