import zmq
import json
from core.notification_manager import NotificationManager
from core.config import load_config

def start_notification_worker(running_check=lambda: True):
    """Запуск обработчика уведомлений"""
    config = load_config()
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect(config["zeromq"]["host"])

    notifier = NotificationManager()
    
    # Устанавливаем таймаут для recv
    socket.setsockopt(zmq.RCVTIMEO, 1000)

    print("[Notification Worker] Ожидание событий...")
    while running_check():
        try:
            data = socket.recv_json()
            
            # Выводим только ответ LLM без технических деталей
            if data.get('type') == 'llm_response' and 'response' in data:
                print(f"\n[LLM] Analysis: {data['response']}")
            else:
                # Для остальных сообщений выводим только основную информацию
                print(f"Получены данные: {data}")
                
            # Определяем severity на основе типа события или сообщения
            severity = "info"
            if "type" in data and data["type"] == "events":
                if "reason" in data and "failed" in data["reason"].lower():
                    severity = "critical"
                elif "reason" in data and "warning" in data["reason"].lower():
                    severity = "warning"
            notifier.notify(str(data), severity)
        except zmq.error.Again:
            continue
        except Exception as e:
            print(f"[Notification Worker] Ошибка: {str(e)}")
    
    print("[Notification Worker] Завершение работы...")
    socket.close()
    context.term()

if __name__ == "__main__":
    start_notification_worker()
