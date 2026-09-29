from pydantic import BaseModel

from typing import List, Optional


class ItineraryRequest(BaseModel):

    destination: str

    trip_days: Optional[int] = None

    traveler_type: Optional[str] = None

    interests: List[str] = []


class RecommendationRequest(BaseModel):

    preferences: str

    budget: Optional[float] = None

    trip_days: Optional[int] = None

    top_k: int = 5


class NearbyRequest(BaseModel):

    destination: str

    radius_km: float = 300

    top_k: int = 5


class ChatRequest(BaseModel):

    message: str