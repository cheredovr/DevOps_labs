# src/api.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI(title="Spam Classifier API", description="API для классификации SMS-сообщений")

# Глобальная переменная для нашей модели
model = None


# Описываем, как должен выглядеть входящий запрос
class MessageRequest(BaseModel):
    text: str


# Описываем ответ
class MessageResponse(BaseModel):
    text: str
    prediction: str


@app.on_event("startup")
def load_model():
    global model
    # Загружаем модель при старте сервера
    model = joblib.load('models/spam_classifier.pkl')
    print("Модель успешно загружена!")


@app.post("/predict", response_model=MessageResponse)
def predict(request: MessageRequest):
    # Делаем предсказание (возвращается список, берем первый элемент)
    prediction = model.predict([request.text])[0]

    return MessageResponse(
        text=request.text,
        prediction=prediction
    )