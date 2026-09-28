class TouristProfile:

    def __init__(
        self,
        travel_style,
        traveler_type,
        interests,
        budget,
        trip_days,
        crowd_preference
    ):

        self.travel_style = travel_style

        self.traveler_type = traveler_type

        self.interests = interests

        self.budget = budget

        self.trip_days = trip_days

        self.crowd_preference = crowd_preference


    def build_preference_text(self):

        interests_text = " ".join(
            self.interests
        )

        preference_text = (
            f"{self.travel_style} "
            f"{self.traveler_type} "
            f"{interests_text} "
            f"{self.crowd_preference}"
        )

        return preference_text