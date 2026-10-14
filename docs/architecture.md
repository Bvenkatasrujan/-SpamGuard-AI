# SpamGuard AI Architecture

SpamGuard AI is designed with strict layer separation:

```mermaid
flowchart TD
    A[Generic Message Text] --> B[Text Normalization]
    B --> C[Word TF-IDF Vectorizer 1,2]
    B --> D[Char TF-IDF Vectorizer 3,5]
    B --> E[Structural & Security Extractor]

    C --> F[Hybrid Feature Matrix]
    D --> F
    E --> F

    F --> G[Calibrated Linear SVM Model]
    G --> H[Spam Probability Score]

    H --> I[Risk Engine]
    H --> J[Security Indicators Engine]

    I --> K[SpamGuard Result Object]
    J --> K

    K --> L[Python SDK]
    K --> M[FastAPI REST API]
    M --> N[React TypeScript Web App]
    M --> O[External Microservices]
```

## Layers

1. **ML Engine Layer (`spamguard/`)**: Pure Python/scikit-learn NLP feature extraction, text normalization, and Platt-scaled SVM probability inference.
2. **REST Service Layer (`backend/`)**: FastAPI HTTP endpoints exposing `/api/v1/predict`, `/api/v1/predict/batch`, and `/api/v1/model`.
3. **Web Client Layer (`frontend/`)**: Vite + React + TypeScript + Tailwind CSS user interface communicating exclusively via HTTP API.
