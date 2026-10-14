"""
Model Information & Config Endpoints for SpamGuard AI REST API.
"""

from fastapi import APIRouter
from backend.app.schemas.prediction import ConfigResponse
from backend.app.services.spamguard_service import get_spamguard
from spamguard.config import SpamGuardConfig
import spamguard

router = APIRouter()

@router.get("/model", tags=["Model"])
def get_model_info():
    """
    Returns active trained model metadata, validation metrics, and feature configuration.
    """
    guard = get_spamguard()
    return guard.get_model_metadata()

@router.get("/config", response_model=ConfigResponse, tags=["Configuration"])
def get_config():
    """
    Returns active SpamGuard system configuration options.
    """
    return ConfigResponse(
        version=spamguard.__version__,
        uncertainty_threshold=SpamGuardConfig.DEFAULT_UNCERTAINTY_THRESHOLD,
        max_message_length=SpamGuardConfig.MAX_MESSAGE_LENGTH,
        url_shorteners=SpamGuardConfig.URL_SHORTENERS
    )
