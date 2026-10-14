"""
Security and Suspicious Indicator Detection Module for SpamGuard AI.
Provides rule-based explanatory indicators to complement model predictions.
"""

import re
from typing import List
from spamguard.config import SpamGuardConfig
from spamguard.features import extract_single_text_metadata
from spamguard.types import TextMetadata

PROMOTIONAL_KEYWORDS = {
    "free", "offer", "discount", "bonus", "cash", "reward", "prize", "winner",
    "guaranteed", "claim", "congratulations", "won", "jackpot", "gift"
}

URGENCY_KEYWORDS = {
    "urgent", "immediately", "now", "limited", "expires", "act now", "valid 12 hours",
    "valid 24 hours", "asap", "hurry", "expire"
}

ACCOUNT_SECURITY_KEYWORDS = {
    "verify", "verification", "password", "account", "login", "suspended", "security",
    "passcode", "otp", "unauthorized", "restrict"
}

FINANCIAL_KEYWORDS = {
    "loan", "money", "payment", "bank", "credit", "debit", "card", "billing", "refund",
    "investment", "transfer", "interest"
}

def detect_indicators(text: str, meta: TextMetadata = None) -> List[str]:
    """
    Scans a message for explanatory security indicators.
    Returns human-readable explanation tags for frontend/API consumption.
    """
    if meta is None:
        meta = extract_single_text_metadata(text)
        
    text_lower = text.lower()
    words_set = set(re.findall(r'\b\w+\b', text_lower))
    indicators = []

    # 0. Blacklisted Spam Emails / Domains
    has_blacklisted_email = any(email.lower() in text_lower for email in SpamGuardConfig.SPAM_BLACK_LIST_EMAILS)
    has_blacklisted_domain = any(domain.lower() in text_lower for domain in SpamGuardConfig.SPAM_BLACK_LIST_DOMAINS)
    if has_blacklisted_email or has_blacklisted_domain:
        indicators.append("Known blacklisted spam email/domain detected")

    # 1. Promotional Language
    matched_promo = words_set.intersection(PROMOTIONAL_KEYWORDS)
    if matched_promo:
        indicators.append("Promotional language detected")

    # 2. Urgency Language
    matched_urgency = words_set.intersection(URGENCY_KEYWORDS)
    if matched_urgency or any(phrase in text_lower for phrase in ["act now", "valid 12", "valid 24"]):
        indicators.append("Urgency or time-sensitive language detected")

    # 3. Account / Security Language
    matched_account = words_set.intersection(ACCOUNT_SECURITY_KEYWORDS)
    if matched_account:
        indicators.append("Account or security verification language detected")

    # 4. Financial Language
    matched_financial = words_set.intersection(FINANCIAL_KEYWORDS)
    if matched_financial or meta.currency_symbol_count > 0:
        indicators.append("Financial or payment language detected")

    # 5. External URLs & Shorteners
    if meta.has_shortened_url:
        indicators.append("Known URL shortener detected")
    elif meta.has_url:
        indicators.append("External URL detected")

    # 6. Phone Contact Details
    if meta.phone_number_count > 0:
        indicators.append("Direct call/SMS contact phone number included")

    # 7. Uppercase Obfuscation / Formatting
    if meta.uppercase_ratio > 0.35 and meta.uppercase_count >= 5:
        indicators.append("Excessive uppercase formatting detected")

    # 8. High Exclamation Mark Usage
    if meta.exclamation_count >= 2:
        indicators.append("Multiple exclamation marks detected")

    # 9. Email Header & Subject Line Indicator
    if meta.has_subject_header:
        indicators.append("Email Subject line header structure detected")

    # 10. Email Contact Details / Unsubscribe Link
    if meta.email_count > 0:
        indicators.append("Embedded email address detected")

    if any(phrase in text_lower for phrase in ["unsubscribe", "click here", "opt out", "opt-out", "remove from list"]):
        indicators.append("Generic email marketing or opt-out link phrasing detected")

    return indicators
