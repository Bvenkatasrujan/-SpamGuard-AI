"""
Detailed Evaluation Script for SpamGuard AI.
Generates ROC curve, Precision-Recall curve, Confusion Matrix figures,
and exports comprehensive evaluation JSON reports.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, roc_auc_score, precision_recall_curve, auc
)

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "cleaned_sms.csv"))
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
PIPELINE_PATH = os.path.join(MODELS_DIR, "spamguard_pipeline.joblib")
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
METRICS_DIR = os.path.join(REPORTS_DIR, "metrics")

def evaluate_pipeline():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    X = df['text'].astype(str)
    y = (df['label'] == 'spam').astype(int).values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"Loading pipeline from {PIPELINE_PATH}...")
    pipeline = joblib.load(PIPELINE_PATH)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    rec = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_proba)

    p_curve, r_curve, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = auc(r_curve, p_curve)

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    eval_results = {
        "dataset_test_samples": len(y_test),
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "roc_auc": round(float(roc_auc), 4),
        "pr_auc": round(float(pr_auc), 4),
        "false_positive_count": int(fp),
        "false_negative_count": int(fn),
        "true_positive_count": int(tp),
        "true_negative_count": int(tn),
        "confusion_matrix": [
            [int(tn), int(fp)],
            [int(fn), int(tp)]
        ]
    }

    with open(os.path.join(METRICS_DIR, "final_evaluation.json"), "w") as f:
        json.dump(eval_results, f, indent=2)

    # 1. Plot Confusion Matrix
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
    plt.title('Confusion Matrix on Test Data')
    plt.xlabel('Predicted Label')
    plt.ylabel('Actual Label')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "confusion_matrix.png"), dpi=300)
    plt.close()

    # 2. Plot ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color='#3b82f6', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "roc_curve.png"), dpi=300)
    plt.close()

    # 3. Plot Precision-Recall Curve
    plt.figure(figsize=(6, 5))
    plt.plot(r_curve, p_curve, color='#10b981', lw=2, label=f'PR curve (AUC = {pr_auc:.4f})')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "precision_recall_curve.png"), dpi=300)
    plt.close()

    print(f"Saved evaluation metrics and figures to {METRICS_DIR} and {FIGURES_DIR}")

if __name__ == "__main__":
    evaluate_pipeline()
