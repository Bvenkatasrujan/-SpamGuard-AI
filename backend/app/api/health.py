"""
Health Check Endpoint for SpamGuard AI REST API.
"""

from fastapi import APIRouter
from backend.app.schemas.prediction import HealthResponse
from backend.app.services.spamguard_service import get_spamguard
import spamguard

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    guard = get_spamguard()
    is_loaded = guard.pipeline is not None
    return HealthResponse(
        status="healthy" if is_loaded else "unhealthy",
        model_loaded=is_loaded,
        version=spamguard.__version__
    )
