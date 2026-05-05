import os
import time
from hdfs import InsecureClient


def init_hdfs():
    hdfs_url = os.getenv("HDFS_URL", "http://namenode:9870")
    client = InsecureClient(hdfs_url, user="hadoop")

    # Ждем, пока HDFS выйдет из безопасного режима (Safe Mode)
    print("Ожидание запуска HDFS...")
    time.sleep(10)

    # Создаем папку для логов и данных
    client.makedirs("/logs")
    client.makedirs("/data")

    # Загружаем датасет (Пункт 4 лабы)
    if os.path.exists("data/spam.csv"):
        with open("data/spam.csv", "rb") as f:
            client.write("/data/spam.csv", f, overwrite=True)
        print("Датасет успешно загружен в HDFS: /data/spam.csv")


if __name__ == "__main__":
    init_hdfs()