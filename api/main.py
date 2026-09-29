from fastapi import FastAPI

from api.schemas import (
    ItineraryRequest,
    RecommendationRequest,
    NearbyRequest,
    ChatRequest
)

from data.itinerary_engine import ItineraryEngine

from data.geospatial_engine import GeospatialEngine

from rag.recommendation_engine import (
    TourismRecommendationEngine
)

from rag.rag_chatbot import RAGChatbot


app = FastAPI(
    title="BharatYatraLM API",
    description="India Tourism AI API",
    version="1.0.0"
)


itinerary_engine = ItineraryEngine()

recommendation_engine = (
    TourismRecommendationEngine()
)

geospatial_engine = GeospatialEngine()

rag_chatbot = RAGChatbot()


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

    recommendations = (
        recommendation_engine.recommend(

            preferences=request.preferences,

            budget=request.budget,

            trip_days=request.trip_days,

            top_k=request.top_k
        )
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
def chat(
    request: ChatRequest
):

    result = rag_chatbot.answer(
        request.message
    )

    return result