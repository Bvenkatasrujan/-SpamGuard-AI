"""
Unit tests for SpamGuard engine detector.
"""

import pytest
from spamguard import SpamGuard
from spamguard.exceptions import InvalidInputError

def test_detector_predict_spam():
    guard = SpamGuard()
    res = guard.predict("URGENT! Congratulations! You won £50,000 cash. Claim at http://bit.ly/prize")
    
    assert res['label'] == 'spam'
    assert res['is_spam'] is True
    assert res['confidence'] >= 0.60
    assert res['risk_level'] in ['high', 'medium']
    assert len(res['indicators']) > 0

def test_detector_predict_ham():
    guard = SpamGuard()
    res = guard.predict("Hey, are we still meeting for lunch at 1 PM today?")
    
    assert res['label'] == 'ham'
    assert res['is_spam'] is False
    assert res['risk_level'] == 'low'

def test_detector_predict_batch():
    guard = SpamGuard()
    messages = [
        "Hey how are you?",
        "URGENT! Free prize money! Claim now at http://bit.ly/win"
    ]
    results = guard.predict_batch(messages)
    
    assert len(results) == 2
    assert results[0]['label'] == 'ham'
    assert results[1]['label'] == 'spam'

def test_detector_empty_text():
    guard = SpamGuard()
    res = guard.predict("")
    assert res['label'] == 'uncertain'
    assert res['is_spam'] is None

def test_detector_predict_email_spam():
    guard = SpamGuard()
    email_text = (
        "Subject: Urgent Security Notice: Password Reset Required\n\n"
        "Dear customer, We detected unusual activity on your banking account. "
        "Please click the link below to verify your password immediately: "
        "http://cheap-phish-domain.biz/verify. Unsubscribe from notifications."
    )
    res = guard.predict(email_text)
    assert res['label'] == 'spam'
    assert res['is_spam'] is True
    assert res['metadata']['is_email'] is True
    assert res['metadata']['has_subject_header'] is True

def test_detector_predict_email_ham():
    guard = SpamGuard()
    email_text = (
        "Subject: Weekly Team Sprint Notes\n\n"
        "Hi team, Here is the summary for this week's progress. "
        "Our launch plan is on track for Thursday. Let me know if you have any questions."
    )
    res = guard.predict(email_text)
    assert res['label'] == 'ham'
    assert res['is_spam'] is False
    assert res['metadata']['is_email'] is True
    assert res['metadata']['has_subject_header'] is True

def test_detector_blacklisted_email_spam():
    guard = SpamGuard()
    res1 = guard.predict("Please contact abc@don.com for your cash reward!")
    res2 = guard.predict("Send your verification details to srujan@abcd.com immediately.")
    
    assert res1['label'] == 'spam'
    assert res1['is_spam'] is True
    assert res1['risk_level'] == 'high'
    assert any("blacklisted" in ind.lower() for ind in res1['indicators'])

    assert res2['label'] == 'spam'
    assert res2['is_spam'] is True
    assert res2['risk_level'] == 'high'
    assert any("blacklisted" in ind.lower() for ind in res2['indicators'])
