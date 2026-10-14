"""
Prediction Endpoints for SpamGuard AI REST API.
"""

from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.prediction import (
    PredictionRequest, PredictionResponse,
    BatchPredictionRequest, BatchPredictionResponse
)
from backend.app.services.spamguard_service import get_spamguard
from spamguard.exceptions import InvalidInputError

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_single(req: PredictionRequest):
    """
    Predict spam probability and security indicators for a single text message.
    """
    guard = get_spamguard()
    try:
        res = guard.predict(req.text)
        return PredictionResponse(**res)
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Prediction error: {str(e)}")

@router.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
def predict_batch(req: BatchPredictionRequest):
    """
    Predict spam probabilities and security indicators for multiple text messages in batch.
    """
    if len(req.messages) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch limit exceeded. Maximum 100 messages allowed per batch request."
        )
    guard = get_spamguard()
    try:
        results = guard.predict_batch(req.messages)
        return BatchPredictionResponse(
            count=len(results),
            results=[PredictionResponse(**r) for r in results]
        )
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Batch error: {str(e)}")
