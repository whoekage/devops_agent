import zmq
import json
from core.notification_manager import NotificationManager
from core.config import load_config

def start_notification_worker():
    """Запуск обработчика уведомлений"""
    config = load_config()
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect(config["zeromq"]["host"])

    notifier = NotificationManager()

    print("Ожидание событий для нотификаций...")
    while True:
        message = socket.recv_json()
        print("\nПолучены данные:", message)

        # Определяем severity на основе типа события или сообщения
        severity = "info"
        if "type" in message and message["type"] == "events":
            if "reason" in message and "failed" in message["reason"].lower():
                severity = "critical"
            elif "reason" in message and "warning" in message["reason"].lower():
                severity = "warning"
        notifier.notify(str(message), severity)

if __name__ == "__main__":
    start_notification_worker()
