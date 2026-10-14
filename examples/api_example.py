"""
Example script demonstrating SpamGuard REST API usage via HTTP requests.
"""

import requests

API_URL = "http://localhost:8000/api/v1/predict"

def main():
    print("Sending POST request to SpamGuard REST API...")
    payload = {
        "text": "URGENT! Congratulations! You won £50,000. Claim at http://bit.ly/prize"
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        print("\n--- REST API Response ---")
        print("Label      :", data["label"])
        print("Confidence :", f"{data['confidence'] * 100:.1f}%")
        print("Risk Level :", data["risk_level"])
        print("Indicators :", data["indicators"])
    except Exception as e:
        print(f"API request failed: {e}. Is FastAPI running on port 8000?")

if __name__ == "__main__":
    main()
