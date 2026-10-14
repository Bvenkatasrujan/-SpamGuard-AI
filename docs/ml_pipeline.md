# SpamGuard Machine Learning & NLP Pipeline

## Feature Engineering

SpamGuard uses a **Hybrid NLP representation**:

1. **Word-level TF-IDF**: Captures semantic/lexical patterns using unigrams and bigrams (`ngram_range=(1,2)`).
2. **Character-level TF-IDF**: Captures obfuscated words (e.g. `FR33`, `C0ngratulati0ns`) and character patterns using character n-grams (`ngram_range=(3,5)`).
3. **Structural & Security Features**: Computes 23 structural and numerical signals (digit ratio, uppercase ratio, exclamation marks, URL shorteners, domain length, phone numbers).

## TF-IDF Formulation

For term $t$ in document $d$:

$$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \text{IDF}(t)$$

$$\text{IDF}(t) = \log\left(\frac{1 + N}{1 + \text{DF}(t)}\right) + 1$$

## Model Benchmarks

Empirical 5-fold Stratified Cross-Validation on UCI SMS Spam Collection dataset:

| Rank | Feature Configuration | Classifier Model | Validation Spam F1 | Precision | Recall | Accuracy |
|---|---|---|---|---|---|---|
| **#1** | **Hybrid NLP + Structural** | **Calibrated Linear SVM** | **95.48%** | **98.78%** | **92.42%** | **98.91%** |
| #2 | Word + Char TF-IDF | Linear SVM | 94.95% | 98.74% | 91.44% | 98.79% |
| #3 | Word TF-IDF | Linear SVM | 94.92% | 97.37% | 92.61% | 98.76% |
| #4 | Char TF-IDF | Linear SVM | 94.41% | 98.72% | 90.47% | 98.67% |
| #5 | Hybrid NLP + Structural | Naive Bayes | 94.39% | 95.49% | 93.39% | 98.62% |

## Held-Out Test Set Results (20% Split)

- **Accuracy**: 99.32%
- **Precision (Spam)**: 100.00% (0 False Positives)
- **Recall (Spam)**: 94.53%
- **Spam F1 Score**: 97.19%
- **ROC-AUC**: 99.88%
- **PR-AUC**: 99.35%
