"""
Configuration Management for SpamGuard AI Engine.
"""

import os

class SpamGuardConfig:
    DEFAULT_UNCERTAINTY_THRESHOLD: float = 0.60
    MAX_MESSAGE_LENGTH: int = 50000
    DEFAULT_MODEL_PATH: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "models", "spamguard_pipeline.joblib")
    )
    DEFAULT_METADATA_PATH: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "models", "model_metadata.json")
    )

    # Configurable URL Shorteners
    URL_SHORTENERS = [
        "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
        "buff.ly", "adf.ly", "bit.do", "mcaf.ee", "su.pr"
    ]

    # Blacklisted Spam Email Addresses & Domains (User Specified)
    SPAM_BLACK_LIST_EMAILS = [
        "abc@don.com",
        "srujan@abcd.com",
        "admin@phish-bank.com",
        "security@verify-login-alert.com",
        "prize@win-lottery-claims.com",
        "support@account-update-notice.net"
    ]

    SPAM_BLACK_LIST_DOMAINS = [
        "don.com",
        "abcd.com",
        "phish-bank.com",
        "verify-login-alert.com",
        "win-lottery-claims.com"
    ]
