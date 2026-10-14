"""
Unit tests for SpamGuard structural feature extractor.
"""

import pytest
import numpy as np
from spamguard.features import extract_single_text_metadata, StructuralFeatureExtractor

def test_extract_single_text_metadata():
    text = "URGENT! You won £5000 cash reward! Call 09061701461 or visit http://bit.ly/claim"
    meta = extract_single_text_metadata(text)
    
    assert meta.message_length == len(text)
    assert meta.exclamation_count == 2
    assert meta.currency_symbol_count == 1
    assert meta.has_url is True
    assert meta.has_shortened_url is True
    assert meta.phone_number_count >= 1

def test_structural_feature_extractor_transformer():
    texts = [
        "Hello world!",
        "URGENT! Claim free cash now at http://bit.ly/test"
    ]
    extractor = StructuralFeatureExtractor()
    features = extractor.fit_transform(texts)
    
    assert isinstance(features, np.ndarray)
    assert features.shape == (2, 26)
