from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.schemas import (
    ItineraryRequest,
    RecommendationRequest,
    NearbyRequest,
    ChatRequest
)
from api.request_handler import TourismRequestHandler
from data.itinerary_engine import ItineraryEngine
from data.geospatial_engine import GeospatialEngine
from rag.recommendation_engine import TourismRecommendationEngine
from rag.rag_chatbot import RAGChatbot
import json
import re

app = FastAPI(
    title="BharatYatraLM API",
    description="India Tourism AI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

with open(
    "data/india_tourism_dataset.json",
    "r",
    encoding="utf-8"
) as file:
    tourism_data = json.load(file)

request_handler = TourismRequestHandler(
    tourism_data
)

itinerary_engine = ItineraryEngine()
recommendation_engine = TourismRecommendationEngine()
geospatial_engine = GeospatialEngine()
rag_chatbot = RAGChatbot()

def find_destination(message):
    text = message.lower()
    for destination in tourism_data:
        name = destination.get(
            "destination_name",
            ""
        )
        if name and name.lower() in text:
            return destination
    return None

def is_exploration_question(message):
    text = message.lower().strip()
    patterns = [
        r"\bwhat\s+should\s+i\s+explore\b",
        r"\bwhat\s+can\s+i\s+explore\b",
        r"\bwhat\s+places\s+should\s+i\s+explore\b",
        r"\bwhat\s+places\s+can\s+i\s+explore\b",
        r"\bwhat\s+should\s+i\s+see\b",
        r"\bwhat\s+can\s+i\s+see\b",
        r"\bplaces\s+to\s+explore\b",
        r"\bplaces\s+to\s+see\b",
        r"\bthings\s+to\s+explore\b",
        r"\bthings\s+to\s+see\b"
    ]
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False

def build_exploration_answer(destination):
    name = destination.get(
        "destination_name",
        ""
    )
    attractions = destination.get(
        "attractions",
        []
    )
    if not attractions:
        attractions = destination.get(
            "primary_attractions",
            []
        )
    if isinstance(
        attractions,
        str
    ):
        attractions = [
            item.strip()
            for item in attractions.split(",")
            if item.strip()
        ]
    if not attractions:
        return (
            f"I don't have specific attraction "
            f"information available for {name}."
        )
    attraction_text = ", ".join(
        str(item)
        for item in attractions
    )
    return (
        f"If you're exploring {name}, "
        f"some of the main attractions include "
        f"{attraction_text}."
    )

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": "BharatYatraLM"
    }

@app.post("/itinerary")
def generate_itinerary(
    request: ItineraryRequest
):
    result = itinerary_engine.get_itinerary(
        destination_name=request.destination,
        trip_days=request.trip_days,
        interests=request.interests,
        traveler_type=request.traveler_type
    )
    return result

@app.post("/recommend")
def recommend_destinations(
    request: RecommendationRequest
):
    recommendations = recommendation_engine.recommend(
        preferences=request.preferences,
        budget=request.budget,
        trip_days=request.trip_days,
        top_k=request.top_k
    )
    return {
        "status": "success",
        "preferences": request.preferences,
        "budget": request.budget,
        "trip_days": request.trip_days,
        "recommendations": recommendations
    }

@app.post("/nearby")
def find_nearby_destinations(
    request: NearbyRequest
):
    result = geospatial_engine.find_nearby(
        destination_name=request.destination,
        radius_km=request.radius_km,
        top_k=request.top_k
    )
    return result

@app.post("/chat")
def chat(request: ChatRequest):
    parsed_request = request_handler.process(
        request.message
    )
    intent = parsed_request["intent"]

    if (
        is_exploration_question(
            request.message
        )
    ):
        destination = find_destination(
            request.message
        )
        if destination:
            answer = build_exploration_answer(
                destination
            )
            return {
                "intent": "chat",
                "message": answer,
                "data": {
                    "query": request.message,
                    "destination": destination.get(
                        "destination_name"
                    ),
                    "answer": answer
                }
            }

    if intent == "itinerary":
        result = itinerary_engine.get_itinerary(
            destination_name=parsed_request[
                "destination"
            ],
            trip_days=parsed_request[
                "trip_days"
            ],
            interests=parsed_request[
                "interests"
            ],
            traveler_type=parsed_request[
                "traveler_type"
            ]
        )
        return {
            "intent": "itinerary",
            "message": "Here is your personalized itinerary.",
            "data": result
        }

    if intent == "recommendation":
        recommendations = recommendation_engine.recommend(
            preferences=request.message,
            trip_days=parsed_request[
                "trip_days"
            ],
            top_k=5
        )
        return {
            "intent": "recommendation",
            "message": "Here are some destinations that match your preferences.",
            "data": recommendations
        }

    if intent == "nearby":
        result = geospatial_engine.find_nearby(
            destination_name=parsed_request[
                "destination"
            ],
            radius_km=300,
            top_k=5
        )
        return {
            "intent": "nearby",
            "message": "Here are some nearby destinations.",
            "data": result
        }

    result = rag_chatbot.answer(
        request.message
    )
    return {
        "intent": "chat",
        "message": result.get(
            "answer",
            ""
        ),
        "data": result
    }

app.mount(
    "/",
    StaticFiles(
        directory="frontend",
        html=True
    ),
    name="frontend"
)