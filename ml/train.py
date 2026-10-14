"""
Model Training & Pipeline Serialization Script for SpamGuard AI.
Trains the winning Hybrid NLP + Structural feature pipeline with Calibrated Linear SVM,
evaluates on the untouched 20% test set, and exports model artifacts.
"""

import os
import sys
import json
import datetime
import pandas as pd
import numpy as np
import joblib

# Ensure spamguard package is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, precision_recall_curve, auc
)

from spamguard.preprocessing import clean_for_vectorization
from spamguard.features import StructuralFeatureExtractor

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "cleaned_sms.csv"))
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
PIPELINE_PATH = os.path.join(MODELS_DIR, "spamguard_pipeline.joblib")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")
FEATURE_CONFIG_PATH = os.path.join(MODELS_DIR, "feature_config.json")

def build_winning_pipeline():
    word_tfidf = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=4000,
        preprocessor=clean_for_vectorization
    )
    char_tfidf = TfidfVectorizer(
        analyzer='char',
        ngram_range=(3, 5),
        max_features=4000
    )
    struct_pipeline = Pipeline([
        ('extractor', StructuralFeatureExtractor()),
        ('scaler', MinMaxScaler())
    ])

    hybrid_features = FeatureUnion([
        ('word_tfidf', word_tfidf),
        ('char_tfidf', char_tfidf),
        ('structural', struct_pipeline)
    ])

    base_svm = LinearSVC(C=1.0, random_state=42, dual=False)
    calibrated_svm = CalibratedClassifierCV(base_svm, cv=3)

    pipeline = Pipeline([
        ('features', hybrid_features),
        ('classifier', calibrated_svm)
    ])
    return pipeline

def train_and_export():
    os.makedirs(MODELS_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    X = df['text'].astype(str)
    y = (df['label'] == 'spam').astype(int).values

    print(f"Loaded {len(df)} records for final model training.")

    # Stratified 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print("Fitting winning Hybrid NLP + Structural Calibrated Linear SVM pipeline on 80% training data...")
    pipeline = build_winning_pipeline()
    pipeline.fit(X_train, y_train)

    print("Evaluating winning pipeline on untouched 20% test dataset...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, pos_label=1, zero_division=0))
    rec = float(recall_score(y_test, y_pred, pos_label=1, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, pos_label=1, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_proba))

    p_curve, r_curve, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = float(auc(r_curve, p_curve))

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    print("\n--- Final Untouched Test Set Results ---")
    print(f"Accuracy         : {acc:.4f}")
    print(f"Precision (Spam) : {prec:.4f}")
    print(f"Recall (Spam)    : {rec:.4f}")
    print(f"F1 Score (Spam)  : {f1:.4f}")
    print(f"ROC-AUC          : {roc_auc:.4f}")
    print(f"PR-AUC           : {pr_auc:.4f}")
    print(f"Confusion Matrix : TP={tp}, FP={fp}, TN={tn}, FN={fn}")

    # Retrain pipeline on full dataset for maximum production quality
    print("\nRetraining final pipeline on complete dataset (100% data) for production deployment...")
    final_pipeline = build_winning_pipeline()
    final_pipeline.fit(X, y)

    # Save serialized pipeline
    joblib.dump(final_pipeline, PIPELINE_PATH)
    print(f"Saved trained pipeline to {PIPELINE_PATH}")

    # Save feature config
    feature_config = {
        "word_ngram_range": [1, 2],
        "word_max_features": 4000,
        "char_ngram_range": [3, 5],
        "char_max_features": 4000,
        "structural_features_count": 26,
        "normalization": "clean_for_vectorization + MinMaxScaler"
    }
    with open(FEATURE_CONFIG_PATH, "w") as f:
        json.dump(feature_config, f, indent=2)

    # Save model metadata
    model_metadata = {
        "model_name": "Calibrated Linear SVM (Hybrid NLP + Structural)",
        "algorithm": "LinearSVC with CalibratedClassifierCV (Platt Scaling)",
        "feature_configuration": "Word TF-IDF (1,2) + Char TF-IDF (3,5) + Structural Security Features",
        "dataset": "Combined UCI SMS Spam Collection & Enron Email Spam Benchmark Dataset",
        "version": "1.0.0",
        "training_date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "cross_validation": {
            "folds": 5,
            "metric": "Spam F1 Score"
        },
        "metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "pr_auc": round(pr_auc, 4),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp),
            "true_negatives": int(tn)
        }
    }
    with open(METADATA_PATH, "w") as f:
        json.dump(model_metadata, f, indent=2)
    print(f"Saved model metadata to {METADATA_PATH}")

if __name__ == "__main__":
    train_and_export()
