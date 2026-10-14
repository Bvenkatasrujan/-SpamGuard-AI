"""
Unit tests for SpamGuard preprocessing module.
"""

import pytest
from spamguard.preprocessing import normalize_text, clean_for_vectorization

def test_normalize_text():
    raw = "  Hello   WORLD!! \n  This is   A Test.  "
    expected = "hello world!! this is a test."
    assert normalize_text(raw) == expected
    assert normalize_text("") == ""
    assert normalize_text(None) == ""

def test_clean_for_vectorization():
    text = "FREE Prize! Claim at http://bit.ly/prize call 09061701461 email support@test.com £1000"
    cleaned = clean_for_vectorization(text)
    assert "urltoken" in cleaned
    assert "phonetoken" in cleaned
    assert "emailtoken" in cleaned
    assert "currencytoken" in cleaned
