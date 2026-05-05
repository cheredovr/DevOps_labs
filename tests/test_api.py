# tests/test_api.py
from fastapi.testclient import TestClient
from src.api import app

def test_predict_spam():
    # Конструкция 'with' гарантирует, что сработает startup-ивент и модель загрузится
    with TestClient(app) as client:
        response = client.post("/predict", json={"text": "WINNER! You have been selected for a cash prize! Call now!"})
        assert response.status_code == 200
        assert response.json()["prediction"] == "spam"

def test_predict_ham():
    with TestClient(app) as client:
        response = client.post("/predict", json={"text": "Hey, are we still on for lunch today?"})
        assert response.status_code == 200
        assert response.json()["prediction"] == "ham"