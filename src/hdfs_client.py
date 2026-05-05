import os
import json
from datetime import datetime
from hdfs import InsecureClient

# Настройки из ENV (Пункт 3 лабы)
HDFS_URL = os.getenv("HDFS_URL", "http://namenode:9870")
HDFS_USER = os.getenv("HDFS_USER", "hadoop")


def get_hdfs_client():
    return InsecureClient(HDFS_URL, user=HDFS_USER)


def log_prediction_to_hdfs(text, prediction):
    client = get_hdfs_client()
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "text": text,
        "prediction": prediction
    }

    path = "/logs/predictions.jsonl"
    # Обязательно ensure_ascii=False для поддержки кириллицы
    content = json.dumps(log_data, ensure_ascii=False) + "\n"

    try:
        # Проверяем статус файла
        if client.status(path, strict=False) is None:
            # Создаем новый файл
            client.write(path, content)
            print(f"HDFS: Создан новый файл логов {path}")
        else:
            # Используем write с флагом append=True (вместо несуществующего метода .append)
            client.write(path, content, append=True)
            print(f"HDFS: Запись добавлена в {path}")

    except Exception as e:
        print(f"Ошибка записи в HDFS: {e}")