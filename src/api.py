# src/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.hdfs_client import log_prediction_to_hdfs
import joblib
import logging

# Настроим логирование в консоль, чтобы видеть ошибки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Spam Classifier API", description="API для классификации SMS-сообщений")

model = None


class MessageRequest(BaseModel):
    text: str


class MessageResponse(BaseModel):
    text: str
    prediction: str


@app.on_event("startup")
def load_model():
    global model
    try:
        model = joblib.load('models/spam_classifier.pkl')
        logger.info("Модель успешно загружена!")
    except Exception as e:
        logger.error(f"НЕ УДАЛОСЬ ЗАГРУЗИТЬ МОДЕЛЬ: {e}")
        model = None


@app.post("/predict", response_model=MessageResponse)
def predict(request: MessageRequest):
    prediction = "unknown"

    # 1. Пытаемся получить предсказание
    if model is not None:
        try:
            prediction = model.predict([request.text])[0]
        except Exception as e:
            logger.error(f"Ошибка предсказания: {e}")
            prediction = "model_error"
    else:
        prediction = "no_model_loaded"

    # 2. Главное для Лабораторной №2: Отправляем результат в HDFS
    try:
        log_prediction_to_hdfs(request.text, prediction)
        logger.info(f"Данные успешно записаны в HDFS для текста: {request.text[:20]}...")
    except Exception as e:
        logger.error(f"ОШИБКА HDFS: {e}")

    return MessageResponse(
        text=request.text,
        prediction=prediction
    )