"""
Custom Exceptions for SpamGuard AI Engine.
"""

class SpamGuardException(Exception):
    """Base exception class for SpamGuard AI."""
    pass

class ModelNotFoundError(SpamGuardException):
    """Raised when model weights/pipeline artifact cannot be loaded."""
    pass

class InvalidInputError(SpamGuardException):
    """Raised when input text is empty, invalid, or exceeds size limits."""
    pass

class FeatureExtractionError(SpamGuardException):
    """Raised when feature extraction fails."""
    pass
