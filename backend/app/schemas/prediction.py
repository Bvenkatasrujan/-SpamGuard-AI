"""
Pydantic Schemas for FastAPI REST Endpoints.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    text: str = Field(
        ...,
        description="Raw text message to classify for spam and security risks",
        example="Congratulations! You won a free prize. Click here now!"
    )

class BatchPredictionRequest(BaseModel):
    messages: List[str] = Field(
        ...,
        description="List of text messages for batch classification",
        example=["Hello, how are you?", "URGENT! You won a prize!"]
    )

class PredictionResponse(BaseModel):
    label: str = Field(..., example="spam")
    is_spam: Optional[bool] = Field(..., example=True)
    confidence: float = Field(..., example=0.9854)
    risk_level: str = Field(..., example="high")
    indicators: List[str] = Field(..., example=["Promotional language detected", "External URL detected"])
    metadata: Dict[str, Any] = Field(...)

class BatchPredictionResponse(BaseModel):
    count: int = Field(..., example=2)
    results: List[PredictionResponse] = Field(...)

class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    model_loaded: bool = Field(..., example=True)
    version: str = Field(..., example="1.0.0")

class ConfigResponse(BaseModel):
    version: str
    uncertainty_threshold: float
    max_message_length: int
    url_shorteners: List[str]
