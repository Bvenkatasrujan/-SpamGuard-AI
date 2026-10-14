"""
Data Preparation Script for SpamGuard AI.
Downloads and prepares the official benchmark UCI SMS Spam Collection dataset (5,572 records).
"""

import os
import sys
import io
import zipfile
import urllib.request
import pandas as pd

DATA_RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw"))
DATA_PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))

RAW_SMS_CSV_PATH = os.path.join(DATA_RAW_DIR, "spam.csv")
RAW_EMAIL_CSV_PATH = os.path.join(DATA_RAW_DIR, "spam_email.csv")
PROCESSED_CSV_PATH = os.path.join(DATA_PROCESSED_DIR, "cleaned_sms.csv")

UCI_SMS_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
ENRON_EMAIL_URL = "https://raw.githubusercontent.com/kristinlussi/DATA_607/main/Project4/spam_ham_dataset.csv"

def prepare_dataset():
    os.makedirs(DATA_RAW_DIR, exist_ok=True)
    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)

    print("Checking raw dataset availability...")
    # 1. Download UCI SMS dataset
    if not os.path.exists(RAW_SMS_CSV_PATH):
        print(f"Downloading official UCI SMS Spam Collection dataset from {UCI_SMS_URL}...")
        req = urllib.request.Request(UCI_SMS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            zip_content = resp.read()
            
        zf = zipfile.ZipFile(io.BytesIO(zip_content))
        with zf.open('SMSSpamCollection') as f:
            df_sms_raw = pd.read_csv(f, sep='\t', header=None, names=['label', 'text'], encoding='utf-8')
        
        df_sms_raw.to_csv(RAW_SMS_CSV_PATH, index=False)
        print(f"Downloaded and saved raw SMS dataset to {RAW_SMS_CSV_PATH} ({len(df_sms_raw)} records).")

    # 2. Download Email Spam dataset
    if not os.path.exists(RAW_EMAIL_CSV_PATH):
        print(f"Downloading benchmark Email Spam dataset from {ENRON_EMAIL_URL}...")
        req = urllib.request.Request(ENRON_EMAIL_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            email_content = resp.read()
        
        df_email_raw = pd.read_csv(io.BytesIO(email_content))
        df_email_raw.to_csv(RAW_EMAIL_CSV_PATH, index=False)
        print(f"Downloaded and saved raw Email dataset to {RAW_EMAIL_CSV_PATH} ({len(df_email_raw)} records).")

    # Load SMS Data
    df_sms = pd.read_csv(RAW_SMS_CSV_PATH)
    if 'v1' in df_sms.columns and 'v2' in df_sms.columns:
        df_sms = df_sms.rename(columns={'v1': 'label', 'v2': 'text'})
    df_sms = df_sms[['label', 'text']].dropna().copy()
    df_sms['source'] = 'sms'

    # Load Email Data
    df_email = pd.read_csv(RAW_EMAIL_CSV_PATH)
    if 'label' in df_email.columns and 'text' in df_email.columns:
        df_email = df_email[['label', 'text']].dropna().copy()
    elif 'v1' in df_email.columns and 'v2' in df_email.columns:
        df_email = df_email.rename(columns={'v1': 'label', 'v2': 'text'})[['label', 'text']].dropna().copy()
    df_email['source'] = 'email'

    # Concatenate datasets and add explicit user-specified blacklisted email spam samples
    custom_spam_samples = pd.DataFrame([
        {"label": "spam", "text": "URGENT! Contact abc@don.com immediately to claim your free cash prize reward of $5,000!", "source": "email"},
        {"label": "spam", "text": "ALERT: Your account is suspended. Verify password with srujan@abcd.com now.", "source": "email"},
        {"label": "spam", "text": "Send bitcoin transfer request to abc@don.com for double returns guaranteed!", "source": "sms"},
        {"label": "spam", "text": "Contact srujan@abcd.com for instant loan approval with zero collateral required.", "source": "sms"},
        {"label": "spam", "text": "Phishing warning: login credentials requested from admin@phish-bank.com.", "source": "email"},
        {"label": "spam", "text": "Claim $100,000 lottery jackpot by emailing security@verify-login-alert.com.", "source": "email"}
    ])

    df = pd.concat([df_sms, df_email, custom_spam_samples], ignore_index=True)
    df['label'] = df['label'].astype(str).str.lower().str.strip()
    df['text'] = df['text'].astype(str).str.strip()
    df = df[df['text'].str.len() > 0]
    df = df.drop_duplicates(subset=['text']).reset_index(drop=True)

    df.to_csv(PROCESSED_CSV_PATH, index=False)
    print(f"\nProcessed dataset saved to {PROCESSED_CSV_PATH}")
    print(f"Total clean non-duplicate records: {len(df)}")
    print(f"Source distribution:\n{df['source'].value_counts()}")
    print(f"Class distribution:\n{df['label'].value_counts()}")
    print(f"Class percentages:\n{df['label'].value_counts(normalize=True) * 100}")
    return df

if __name__ == "__main__":
    prepare_dataset()

