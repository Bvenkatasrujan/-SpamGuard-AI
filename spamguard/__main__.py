"""
CLI Entry point for SpamGuard AI Engine.
Enables command line classification:
$ python -m spamguard "Message text here"
"""

import sys
import argparse
from spamguard.detector import SpamGuard

def main():
    parser = argparse.ArgumentParser(
        description="SpamGuard AI - Command Line Interface for Hybrid NLP Spam Classification"
    )
    parser.add_argument(
        "text",
        type=str,
        nargs="?",
        help="Text message to analyze for spam and security risks"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.60,
        help="Uncertainty threshold score (default 0.60)"
    )

    args = parser.parse_args()

    if not args.text:
        print("Usage: python -m spamguard \"Your text message here\"")
        sys.exit(1)

    try:
        guard = SpamGuard(uncertainty_threshold=args.threshold)
        res = guard.predict(args.text)

        label_display = res['label'].upper()
        confidence_pct = f"{int(round(res['confidence'] * 100))}%"
        risk_display = res['risk_level'].upper()

        print("\n==========================================")
        print("           SPAMGUARD AI REPORT            ")
        print("==========================================")
        print(f"Prediction : {label_display}")
        print(f"Confidence : {confidence_pct}")
        print(f"Risk       : {risk_display}")
        print("------------------------------------------")
        if res['indicators']:
            print("Security Indicators Detected:")
            for ind in res['indicators']:
                print(f"  • {ind}")
        else:
            print("Security Indicators Detected: None")
        print("==========================================\n")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
