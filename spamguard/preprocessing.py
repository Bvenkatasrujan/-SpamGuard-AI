"""
Text Preprocessing and Normalization Module for SpamGuard AI.
"""

import re
import string
from typing import List

URL_PATTERN = re.compile(r'https?://\S+|www\.\S+', re.IGNORECASE)
PHONE_PATTERN = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{10,13}|0\d{10}')
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
CURRENCY_PATTERN = re.compile(r'[$£€₹¥]')

def normalize_text(text: str) -> str:
    """
    Normalizes input text for NLP vectorizers.
    Lowercases text, standardizes whitespace, and normalizes unicode/formatting.
    """
    if not text:
        return ""
    
    # Strip whitespace
    normalized = text.strip()
    
    # Lowercase text
    normalized = normalized.lower()
    
    # Standardize whitespace (convert multiple spaces/newlines into single space)
    normalized = re.sub(r'\s+', ' ', normalized)
    
    return normalized

def clean_for_vectorization(text: str) -> str:
    """
    Cleans normalized text for word TF-IDF vectorization.
    """
    text = normalize_text(text)
    # Replace URLs, Emails, Phones with generic tokens for semantic TF-IDF stability
    text = URL_PATTERN.sub(' urltoken ', text)
    text = EMAIL_PATTERN.sub(' emailtoken ', text)
    text = PHONE_PATTERN.sub(' phonetoken ', text)
    text = CURRENCY_PATTERN.sub(' currencytoken ', text)
    
    # Standardize whitespace again
    text = re.sub(r'\s+', ' ', text).strip()
    return text
