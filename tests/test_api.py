"""
Unit tests for FastAPI REST endpoints using TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True

def test_predict_single_endpoint():
    response = client.post(
        "/api/v1/predict",
        json={"text": "URGENT! You won £1000 cash! Claim at http://bit.ly/win"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "spam"
    assert data["is_spam"] is True

def test_predict_batch_endpoint():
    response = client.post(
        "/api/v1/predict/batch",
        json={"messages": ["Hello there", "Free money! Claim now!"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["results"]) == 2

def test_model_info_endpoint():
    response = client.get("/api/v1/model")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
