"""
Dataset EDA & Analysis Script for SpamGuard AI.
Calculates summary statistics and outputs charts to reports/figures/.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "cleaned_sms.csv"))
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
METRICS_DIR = os.path.join(REPORTS_DIR, "metrics")

def analyze_dataset():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} records for analysis.")

    df['length'] = df['text'].astype(str).str.len()
    df['word_count'] = df['text'].astype(str).apply(lambda s: len(s.split()))

    total_count = len(df)
    spam_df = df[df['label'] == 'spam']
    ham_df = df[df['label'] == 'ham']

    stats = {
        "total_messages": total_count,
        "spam_messages": len(spam_df),
        "ham_messages": len(ham_df),
        "spam_percentage": round(len(spam_df) / total_count * 100, 2),
        "ham_percentage": round(len(ham_df) / total_count * 100, 2),
        "avg_message_length": round(df['length'].mean(), 2),
        "avg_spam_length": round(spam_df['length'].mean(), 2),
        "avg_ham_length": round(ham_df['length'].mean(), 2),
        "avg_message_word_count": round(df['word_count'].mean(), 2),
        "avg_spam_word_count": round(spam_df['word_count'].mean(), 2),
        "avg_ham_word_count": round(ham_df['word_count'].mean(), 2)
    }

    print("\nDataset Statistics:")
    print(json.dumps(stats, indent=2))

    # Save stats JSON
    with open(os.path.join(METRICS_DIR, "eda_summary.json"), "w") as f:
        json.dump(stats, f, indent=2)

    # Visualization 1: Class Distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x='label', data=df, palette=['#10b981', '#ef4444'])
    plt.title('Spam vs Ham Class Distribution')
    plt.xlabel('Label')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "class_distribution.png"), dpi=300)
    plt.close()

    # Visualization 2: Message Length Distribution
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x='length', hue='label', bins=50, kde=True, palette=['#10b981', '#ef4444'], element="step")
    plt.title('Message Length Distribution by Class')
    plt.xlabel('Character Length')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "message_length_distribution.png"), dpi=300)
    plt.close()

    # Visualization 3: Word Count Boxplot
    plt.figure(figsize=(6, 4))
    sns.boxplot(x='label', y='word_count', data=df, palette=['#10b981', '#ef4444'])
    plt.title('Word Count Distribution by Class')
    plt.xlabel('Label')
    plt.ylabel('Word Count')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "word_count_boxplot.png"), dpi=300)
    plt.close()

    print("Charts generated successfully in reports/figures/")

if __name__ == "__main__":
    analyze_dataset()
