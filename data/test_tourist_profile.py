from data.tourist_profile import TouristProfile


profile = TouristProfile(
    travel_style="peaceful",
    traveler_type="couple",
    interests=[
        "beaches",
        "nature"
    ],
    budget=10000,
    trip_days=3,
    crowd_preference="fewer crowds"
)


print(
    "Travel style:",
    profile.travel_style
)

print(
    "Traveler type:",
    profile.traveler_type
)

print(
    "Interests:",
    profile.interests
)

print(
    "Budget:",
    profile.budget
)

print(
    "Trip days:",
    profile.trip_days
)

print(
    "Crowd preference:",
    profile.crowd_preference
)


print(
    "\nPreference text:"
)

print(
    profile.build_preference_text()
)