"""
Type Definitions and Data Schemas for SpamGuard AI Engine.
"""

from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field

RiskLevel = Literal["low", "medium", "high", "uncertain"]
LabelType = Literal["ham", "spam", "uncertain"]

@dataclass
class TextMetadata:
    message_length: int
    word_count: int
    character_count: int
    digit_count: int
    digit_ratio: float
    uppercase_count: int
    uppercase_ratio: float
    special_character_count: int
    punctuation_count: int
    exclamation_count: int
    question_mark_count: int
    currency_symbol_count: int
    emoji_count: int
    url_count: int
    phone_number_count: int
    email_count: int
    has_url: bool
    has_http: bool
    has_https: bool
    has_www: bool
    has_shortened_url: bool
    domain_length: int
    subdomain_count: int
    is_email: bool = False
    has_subject_header: bool = False
    line_count: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_length": self.message_length,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "digit_count": self.digit_count,
            "digit_ratio": round(self.digit_ratio, 4),
            "uppercase_count": self.uppercase_count,
            "uppercase_ratio": round(self.uppercase_ratio, 4),
            "special_character_count": self.special_character_count,
            "punctuation_count": self.punctuation_count,
            "exclamation_count": self.exclamation_count,
            "question_mark_count": self.question_mark_count,
            "currency_symbol_count": self.currency_symbol_count,
            "emoji_count": self.emoji_count,
            "url_count": self.url_count,
            "phone_number_count": self.phone_number_count,
            "email_count": self.email_count,
            "has_url": self.has_url,
            "has_shortened_url": self.has_shortened_url,
            "is_email": self.is_email,
            "has_subject_header": self.has_subject_header,
            "line_count": self.line_count
        }

@dataclass
class PredictionResult:
    label: LabelType
    is_spam: Optional[bool]
    confidence: float
    risk_level: RiskLevel
    indicators: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "is_spam": self.is_spam,
            "confidence": round(self.confidence, 4),
            "risk_level": self.risk_level,
            "indicators": self.indicators,
            "metadata": self.metadata
        }
