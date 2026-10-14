"""
Service Singleton for SpamGuard Engine in FastAPI.
"""

from spamguard.detector import SpamGuard

_spamguard_instance = None

def get_spamguard() -> SpamGuard:
    global _spamguard_instance
    if _spamguard_instance is None:
        _spamguard_instance = SpamGuard()
    return _spamguard_instance
