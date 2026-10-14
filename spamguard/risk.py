"""
Risk Assessment Engine for SpamGuard AI.
Maps classifier prediction probabilities and confidence scores to risk levels and uncertainty labels.
"""

from typing import Tuple, Optional
from spamguard.types import RiskLevel, LabelType
from spamguard.config import SpamGuardConfig

def evaluate_risk(
    raw_label: str,
    raw_probability: float,
    uncertainty_threshold: float = SpamGuardConfig.DEFAULT_UNCERTAINTY_THRESHOLD
) -> Tuple[LabelType, Optional[bool], float, RiskLevel]:
    """
    Evaluates risk and uncertainty given raw classifier label ('spam' or 'ham')
    and raw spam probability score [0.0, 1.0].
    
    Returns: (label, is_spam, confidence, risk_level)
    """
    # Calculate confidence as distance from decision boundary 0.5 (scaled to [0.5, 1.0])
    if raw_label == "spam":
        confidence = raw_probability
    else:
        confidence = 1.0 - raw_probability

    # Check uncertainty threshold
    if confidence < uncertainty_threshold:
        return "uncertain", None, confidence, "uncertain"

    if raw_label == "spam":
        is_spam = True
        label = "spam"
        if confidence >= 0.80:
            risk_level = "high"
        else:
            risk_level = "medium"
    else:
        is_spam = False
        label = "ham"
        risk_level = "low"

    return label, is_spam, confidence, risk_level
