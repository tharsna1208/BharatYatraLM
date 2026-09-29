import re


def detect_intent(message):

    text = message.lower().strip()


    itinerary_patterns = [
        r"\bplan\b.*\btrip\b",
        r"\bplan\b.*\btravel\b",
        r"\btrip\s+plan\b",
        r"\btravel\s+plan\b",
        r"\bitinerary\b",
        r"\bschedule\b",
        r"\b\d+\s*day\s+trip\b",
        r"\b\d+\s*days?\b.*\btrip\b",
        r"\bhow\s+many\s+days\b",
        r"\bwhat\s+should\s+i\s+do\b"
    ]


    nearby_patterns = [
        r"\bnearby\b",
        r"\bnear\s+me\b",
        r"\bplaces\s+near\b",
        r"\bdestinations\s+near\b",
        r"\bclose\s+to\b",
        r"\bclose\s+by\b",
        r"\baround\b"
    ]


    recommendation_patterns = [
        r"\brecommend\b",
        r"\brecommendation\b",
        r"\bsuggest\b",
        r"\bsuggestions\b",
        r"\bwhere\s+should\s+i\s+go\b",
        r"\bbest\s+places\b",
        r"\bgood\s+places\b",
        r"\bplaces\s+to\s+visit\b",
        r"\bdestination\s+for\b",
        r"\bdestinations\s+for\b",
        r"\blooking\s+for\b",
        r"\bfind\s+me\b",
        r"\bpeaceful\s+places\b",
        r"\bpeaceful\s+destinations\b",
        r"\bquiet\s+places\b",
        r"\bquiet\s+destinations\b",
        r"\bcalm\s+places\b",
        r"\bcalm\s+destinations\b",
        r"\brelaxing\s+places\b",
        r"\brelaxing\s+destinations\b",
        r"\bbeach\s+places\b",
        r"\bbeach\s+destinations\b",
        r"\bbeaches\b.*\bdestinations\b",
        r"\bmountain\s+places\b",
        r"\bmountain\s+destinations\b",
        r"\bmountains\b.*\bdestinations\b",
        r"\bnature\s+places\b",
        r"\bnature\s+destinations\b",
        r"\badventure\s+places\b",
        r"\badventure\s+destinations\b",
        r"\bcultural\s+places\b",
        r"\bcultural\s+destinations\b",
        r"\bfood\s+destinations\b",
        r"\bnightlife\s+destinations\b"
    ]


    for pattern in itinerary_patterns:

        if re.search(pattern, text):

            return "itinerary"


    for pattern in nearby_patterns:

        if re.search(pattern, text):

            return "nearby"


    for pattern in recommendation_patterns:

        if re.search(pattern, text):

            return "recommendation"


    return "chat"