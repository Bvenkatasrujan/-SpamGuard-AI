"""
Example script demonstrating SpamGuard Python SDK usage.
"""

from spamguard import SpamGuard

def main():
    print("Initializing SpamGuard Python Engine...")
    guard = SpamGuard()

    # Test 1: Single Prediction (Spam)
    spam_msg = "URGENT! Congratulations! You won ₹50,000 cash reward. Claim at http://bit.ly/claim-prize"
    print(f"\nScanning Message: '{spam_msg}'")
    res1 = guard.predict(spam_msg)
    print(f"Prediction : {res1['label'].upper()}")
    print(f"Confidence : {res1['confidence'] * 100:.1f}%")
    print(f"Risk Level : {res1['risk_level'].upper()}")
    print("Indicators :", res1['indicators'])

    # Test 2: Single Prediction (Ham)
    ham_msg = "Hi, are you coming to college tomorrow for the machine learning lecture?"
    print(f"\nScanning Message: '{ham_msg}'")
    res2 = guard.predict(ham_msg)
    print(f"Prediction : {res2['label'].upper()}")
    print(f"Confidence : {res2['confidence'] * 100:.1f}%")
    print(f"Risk Level : {res2['risk_level'].upper()}")

    # Test 3: Batch Prediction
    batch = [
        "Hey! What time are we meeting?",
        "FR33 PRIZE! Call 09061701461 to claim your £1000 cash now!"
    ]
    print("\nBatch Scanning Messages...")
    batch_results = guard.predict_batch(batch)
    for i, r in enumerate(batch_results):
        print(f"Message {i+1}: {r['label'].upper()} ({r['confidence']*100:.1f}%)")

if __name__ == "__main__":
    main()
