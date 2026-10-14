"""
SpamGuard AI Package Initialization.
"""

from spamguard.detector import SpamGuard
from spamguard.config import SpamGuardConfig
from spamguard.types import PredictionResult, TextMetadata, RiskLevel, LabelType
from spamguard.exceptions import SpamGuardException, ModelNotFoundError, InvalidInputError

__version__ = "1.0.0"
__all__ = [
    "SpamGuard",
    "SpamGuardConfig",
    "PredictionResult",
    "TextMetadata",
    "RiskLevel",
    "LabelType",
    "SpamGuardException",
    "ModelNotFoundError",
    "InvalidInputError"
]
