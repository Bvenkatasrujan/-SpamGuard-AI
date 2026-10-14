"""
Feature Engineering Module for SpamGuard AI.
Extracts 23 structural, numerical, punctuation, URL, domain, and security signals from raw text.
Implements scikit-learn BaseEstimator and TransformerMixin for seamless Pipeline integration.
"""

import re
import string
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from urllib.parse import urlparse
from sklearn.base import BaseEstimator, TransformerMixin
from spamguard.config import SpamGuardConfig
from spamguard.types import TextMetadata

URL_REGEX = re.compile(r'https?://[^\s]+|www\.[^\s]+', re.IGNORECASE)
PHONE_REGEX = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{10,13}|0\d{10}')
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
CURRENCY_REGEX = re.compile(r'[$£€₹¥]')

def extract_single_text_metadata(text: str) -> TextMetadata:
    """Extracts raw metadata dataclass from a single string message."""
    if not isinstance(text, str):
        text = str(text) if text is not None else ""
        
    char_count = len(text)
    words = text.split()
    word_count = len(words)
    
    digit_count = sum(c.isdigit() for c in text)
    digit_ratio = (digit_count / char_count) if char_count > 0 else 0.0
    
    uppercase_count = sum(c.isupper() for c in text)
    uppercase_ratio = (uppercase_count / char_count) if char_count > 0 else 0.0
    
    punct_count = sum(c in string.punctuation for c in text)
    excl_count = text.count('!')
    qmark_count = text.count('?')
    currency_count = len(CURRENCY_REGEX.findall(text))
    
    # Emojis or non-ascii printable characters
    emoji_count = len([c for c in text if ord(c) > 127])
    special_char_count = punct_count + currency_count + emoji_count
    
    urls = URL_REGEX.findall(text)
    url_count = len(urls)
    has_url = url_count > 0
    has_http = any('http://' in u.lower() for u in urls)
    has_https = any('https://' in u.lower() for u in urls)
    has_www = any('www.' in u.lower() for u in urls)
    
    has_shortened_url = False
    domain_length = 0
    subdomain_count = 0
    
    for u in urls:
        formatted_url = u if u.lower().startswith(('http://', 'https://')) else 'http://' + u
        try:
            parsed = urlparse(formatted_url)
            netloc = parsed.netloc.lower()
            if any(shortener in netloc for shortener in SpamGuardConfig.URL_SHORTENERS):
                has_shortened_url = True
            if netloc:
                domain_length = max(domain_length, len(netloc))
                subdomain_count = max(subdomain_count, len(netloc.split('.')) - 2)
        except Exception:
            pass
            
    phone_count = len(PHONE_REGEX.findall(text))
    email_count = len(EMAIL_REGEX.findall(text))

    has_subject_header = text.lower().startswith('subject:') or '\nsubject:' in text.lower()
    line_count = len(text.splitlines())
    is_email = has_subject_header or line_count > 3 or char_count > 300 or email_count > 0

    return TextMetadata(
        message_length=char_count,
        word_count=word_count,
        character_count=char_count,
        digit_count=digit_count,
        digit_ratio=digit_ratio,
        uppercase_count=uppercase_count,
        uppercase_ratio=uppercase_ratio,
        special_character_count=special_char_count,
        punctuation_count=punct_count,
        exclamation_count=excl_count,
        question_mark_count=qmark_count,
        currency_symbol_count=currency_count,
        emoji_count=emoji_count,
        url_count=url_count,
        phone_number_count=phone_count,
        email_count=email_count,
        has_url=has_url,
        has_http=has_http,
        has_https=has_https,
        has_www=has_www,
        has_shortened_url=has_shortened_url,
        domain_length=domain_length,
        subdomain_count=max(0, subdomain_count),
        is_email=is_email,
        has_subject_header=has_subject_header,
        line_count=line_count
    )


class StructuralFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    scikit-learn compatible transformer for extracting structural, security,
    and URL features from text input (SMS & Email).
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> np.ndarray:
        if isinstance(X, pd.Series):
            X = X.tolist()
        elif isinstance(X, np.ndarray):
            X = X.tolist()

        features_matrix = []
        for text in X:
            meta = extract_single_text_metadata(text)
            row = [
                meta.message_length,
                meta.word_count,
                meta.character_count,
                meta.digit_count,
                meta.digit_ratio,
                meta.uppercase_count,
                meta.uppercase_ratio,
                meta.special_character_count,
                meta.punctuation_count,
                meta.exclamation_count,
                meta.question_mark_count,
                meta.currency_symbol_count,
                meta.emoji_count,
                meta.url_count,
                meta.phone_number_count,
                meta.email_count,
                1.0 if meta.has_url else 0.0,
                1.0 if meta.has_http else 0.0,
                1.0 if meta.has_https else 0.0,
                1.0 if meta.has_www else 0.0,
                1.0 if meta.has_shortened_url else 0.0,
                float(meta.domain_length),
                float(meta.subdomain_count),
                1.0 if meta.is_email else 0.0,
                1.0 if meta.has_subject_header else 0.0,
                float(meta.line_count)
            ]
            features_matrix.append(row)

        return np.array(features_matrix, dtype=np.float64)
