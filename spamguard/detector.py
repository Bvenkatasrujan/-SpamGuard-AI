"""
SpamGuard Main Engine and Detector API.
Provides high-level SpamGuard class for single and batch text security predictions.
"""

import os
import json
import joblib
from typing import List, Dict, Any, Union

from spamguard.config import SpamGuardConfig
from spamguard.exceptions import ModelNotFoundError, InvalidInputError
from spamguard.features import extract_single_text_metadata
from spamguard.indicators import detect_indicators
from spamguard.risk import evaluate_risk
from spamguard.types import PredictionResult

class SpamGuard:
    """
    Main reusable SpamGuard AI Engine.
    
    Example:
        >>> from spamguard import SpamGuard
        >>> guard = SpamGuard()
        >>> result = guard.predict("Congratulations! You won a free prize.")
        >>> print(result['label'], result['confidence'])
    """
    def __init__(
        self,
        model_path: str = None,
        uncertainty_threshold: float = SpamGuardConfig.DEFAULT_UNCERTAINTY_THRESHOLD
    ):
        self.model_path = model_path or SpamGuardConfig.DEFAULT_MODEL_PATH
        self.metadata_path = SpamGuardConfig.DEFAULT_METADATA_PATH
        self.uncertainty_threshold = uncertainty_threshold
        self.pipeline = None
        self.metadata = {}
        
        self._load_pipeline()

    def _load_pipeline(self):
        if not os.path.exists(self.model_path):
            raise ModelNotFoundError(
                f"Model pipeline file not found at {self.model_path}. "
                "Please run `python ml/train.py` to train and save the pipeline."
            )
        try:
            self.pipeline = joblib.load(self.model_path)
        except Exception as e:
            raise ModelNotFoundError(f"Failed to load SpamGuard pipeline artifact: {e}")

        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, "r") as f:
                    self.metadata = json.load(f)
            except Exception:
                self.metadata = {}

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Analyzes a single generic text message (SMS, Email, Chat, Form, etc.)
        and returns a structured prediction dictionary.
        """
        if text is None:
            raise InvalidInputError("Message text cannot be None.")
            
        if not isinstance(text, str):
            text = str(text)

        cleaned = text.strip()
        if len(cleaned) == 0:
            # Handle empty string gracefully
            meta = extract_single_text_metadata("")
            return PredictionResult(
                label="uncertain",
                is_spam=None,
                confidence=0.50,
                risk_level="uncertain",
                indicators=["Empty text input"],
                metadata=meta.to_dict()
            ).to_dict()

        if len(text) > SpamGuardConfig.MAX_MESSAGE_LENGTH:
            raise InvalidInputError(f"Message exceeds maximum allowed length of {SpamGuardConfig.MAX_MESSAGE_LENGTH} characters.")

        # 1. Feature Extraction & Model Inference
        proba = self.pipeline.predict_proba([text])[0]
        spam_prob = float(proba[1])

        text_lower = text.lower()
        has_blacklisted_email = any(e.lower() in text_lower for e in SpamGuardConfig.SPAM_BLACK_LIST_EMAILS)
        has_blacklisted_domain = any(d.lower() in text_lower for d in SpamGuardConfig.SPAM_BLACK_LIST_DOMAINS)
        
        if has_blacklisted_email or has_blacklisted_domain:
            spam_prob = max(spam_prob, 0.99)

        raw_label = "spam" if spam_prob >= 0.50 else "ham"

        # 2. Risk & Uncertainty Evaluation
        label, is_spam, confidence, risk_level = evaluate_risk(
            raw_label=raw_label,
            raw_probability=spam_prob,
            uncertainty_threshold=self.uncertainty_threshold
        )

        # 3. Security Indicators & Metadata Extraction
        meta = extract_single_text_metadata(text)
        indicators = detect_indicators(text, meta)

        result = PredictionResult(
            label=label,
            is_spam=is_spam,
            confidence=confidence,
            risk_level=risk_level,
            indicators=indicators,
            metadata=meta.to_dict()
        )
        return result.to_dict()

    def predict_batch(self, messages: List[str]) -> List[Dict[str, Any]]:
        """
        Analyzes a batch of generic text messages efficiently.
        """
        if not isinstance(messages, list):
            raise InvalidInputError("predict_batch requires a list of text strings.")
        return [self.predict(msg) for msg in messages]

    def get_model_metadata(self) -> Dict[str, Any]:
        """Returns loaded model metadata details."""
        return self.metadata
