# Используем официальный легкий образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код и обученную модель в контейнер
COPY src/ /app/src/
COPY models/ /app/models/

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска нашего FastAPI сервера
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]