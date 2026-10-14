"""
Model Comparison & Feature Benchmark Script for SpamGuard AI.
Compares candidate classifiers (Naive Bayes, Logistic Regression, Linear SVM)
across 4 feature configurations on 5-fold Stratified Cross Validation.
"""

import os
import sys
import json
import pandas as pd
import numpy as np

# Ensure spamguard package is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import make_scorer, f1_score, precision_score, recall_score, accuracy_score, roc_auc_score

from spamguard.preprocessing import clean_for_vectorization
from spamguard.features import StructuralFeatureExtractor

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "cleaned_sms.csv"))
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))
CSV_OUTPUT_PATH = os.path.join(REPORTS_DIR, "model_comparison.csv")
METRICS_JSON_PATH = os.path.join(REPORTS_DIR, "metrics", "comparison_summary.json")

def build_feature_pipeline(config_type: str):
    word_tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=4000, preprocessor=clean_for_vectorization)
    char_tfidf = TfidfVectorizer(analyzer='char', ngram_range=(3, 5), max_features=4000)
    struct_pipeline = Pipeline([
        ('extractor', StructuralFeatureExtractor()),
        ('scaler', MinMaxScaler())
    ])

    if config_type == "Word TF-IDF":
        return word_tfidf
    elif config_type == "Char TF-IDF":
        return char_tfidf
    elif config_type == "Word + Char TF-IDF":
        return FeatureUnion([
            ('word', word_tfidf),
            ('char', char_tfidf)
        ])
    elif config_type == "Hybrid NLP + Structural":
        return FeatureUnion([
            ('word', word_tfidf),
            ('char', char_tfidf),
            ('struct', struct_pipeline)
        ])
    else:
        raise ValueError(f"Unknown config_type: {config_type}")

def compare_all_models():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(os.path.join(REPORTS_DIR, "metrics"), exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    X = df['text'].astype(str)
    y = (df['label'] == 'spam').astype(int).values

    # Stratified 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    feature_configs = [
        "Word TF-IDF",
        "Char TF-IDF",
        "Word + Char TF-IDF",
        "Hybrid NLP + Structural"
    ]

    classifiers = {
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.1),
        "Logistic Regression": LogisticRegression(max_iter=1000, C=5.0, random_state=42),
        "Linear SVM": CalibratedClassifierCV(LinearSVC(C=1.0, random_state=42, dual=False), cv=3)
    }

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, pos_label=1, zero_division=0),
        'recall': make_scorer(recall_score, pos_label=1, zero_division=0),
        'f1_spam': make_scorer(f1_score, pos_label=1, zero_division=0),
        'roc_auc': 'roc_auc'
    }

    results = []

    print("Starting 5-Fold Stratified Cross Validation benchmarks...")
    for config_name in feature_configs:
        for clf_name, clf in classifiers.items():
            print(f"Evaluating: [{config_name}] + [{clf_name}]...")
            
            fe_pipe = build_feature_pipeline(config_name)
            full_pipeline = Pipeline([
                ('features', fe_pipe),
                ('classifier', clf)
            ])

            cv_results = cross_validate(
                full_pipeline, X_train, y_train,
                cv=skf, scoring=scoring, n_jobs=-1
            )

            acc_mean = cv_results['test_accuracy'].mean()
            prec_mean = cv_results['test_precision'].mean()
            rec_mean = cv_results['test_recall'].mean()
            f1_mean = cv_results['test_f1_spam'].mean()
            auc_mean = cv_results['test_roc_auc'].mean()

            results.append({
                "Feature Configuration": config_name,
                "Model": clf_name,
                "Accuracy": round(float(acc_mean), 4),
                "Precision (Spam)": round(float(prec_mean), 4),
                "Recall (Spam)": round(float(rec_mean), 4),
                "F1 Score (Spam)": round(float(f1_mean), 4),
                "ROC-AUC": round(float(auc_mean), 4)
            })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="F1 Score (Spam)", ascending=False).reset_index(drop=True)

    print("\n--- Model Comparison Benchmark Results ---")
    print(results_df.to_string())

    results_df.to_csv(CSV_OUTPUT_PATH, index=False)
    print(f"\nSaved CSV benchmark summary to {CSV_OUTPUT_PATH}")

    with open(METRICS_JSON_PATH, "w") as f:
        json.dump(results, f, indent=2)

    return results_df

if __name__ == "__main__":
    compare_all_models()
