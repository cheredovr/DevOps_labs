# src/train.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

# Создаем папку для модели
os.makedirs('models', exist_ok=True)

print("Загрузка данных...")
# Читаем CSV файл. Для spam.csv с Kaggle обычно нужна кодировка latin-1
df = pd.read_csv('data/spam.csv', encoding='latin-1')

# Оставляем только нужные колонки и переименовываем их для удобства
df = df[['v1', 'v2']]
df.columns = ['label', 'message']

print("Обучение модели...")
# Создаем пайплайн: перевод текста в числа (TF-IDF) + Логистическая регрессия
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=3000)),
    ('clf', LogisticRegression())
])

# Обучаем модель
pipeline.fit(df['message'], df['label'])

# Сохраняем модель
model_path = 'models/spam_classifier.pkl'
joblib.dump(pipeline, model_path)

print(f"Успех! Модель сохранена в {model_path}")