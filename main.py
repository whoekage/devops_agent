import threading
import signal
import sys
from core.config import load_config
from agents.k8s_agent import KubernetesAgent
from workers.llm_worker import start_llm_worker
from workers.notification_worker import start_notification_worker

# Глобальный флаг для сигнализации остановки потоков
running = True

def signal_handler(signum, frame):
    """Обработчик сигнала для graceful shutdown"""
    global running
    print("\n[Main] Получен сигнал остановки. Завершаем работу...")
    running = False

def start_agent(agent_name):
    """Запускает нужного агента, если он включен в config.yaml"""
    config = load_config()
    agent_config = next((a for a in config["agents"] if a["name"] == agent_name), None)
    
    if not agent_config or not agent_config.get("enabled", False):
        print(f"[Main] Агент {agent_name} отключен, пропускаем...")
        return None

    print(f"[Main] Запускаем {agent_name}...")

    if agent_name == "k8s_agent":
        return threading.Thread(target=KubernetesAgent(config["zeromq"]["host"]).run, 
                              args=(lambda: running,))  # Передаем функцию проверки флага

    print(f"[Main] Неизвестный агент: {agent_name}")
    return None

if __name__ == "__main__":
    # Устанавливаем обработчик сигнала
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    config = load_config()

    # Запускаем агентов
    agent_threads = []
    for agent in config["agents"]:
        agent_thread = start_agent(agent["name"])
        if agent_thread:
            agent_thread.start()
            agent_threads.append(agent_thread)

    # Запускаем обработчики LLM и уведомлений
    print("[Main] Запускаем обработчик LLM...")
    llm_thread = threading.Thread(target=start_llm_worker, 
                                args=(lambda: running,))  # Передаем функцию проверки флага
    llm_thread.start()

    print("[Main] Запускаем обработчик уведомлений...")
    notification_thread = threading.Thread(target=start_notification_worker, 
                                        args=(lambda: running,))  # Передаем функцию проверки флага
    notification_thread.start()

    # Ожидаем завершения всех потоков
    try:
        while running:
            for thread in agent_threads + [llm_thread, notification_thread]:
                thread.join(timeout=0.5)  # Проверяем состояние потоков каждые 0.5 секунд
    except KeyboardInterrupt:
        print("\n[Main] Получено прерывание клавиатуры. Завершаем работу...")
        running = False

    print("[Main] Ожидаем завершения всех потоков...")
    for thread in agent_threads + [llm_thread, notification_thread]:
        thread.join()
    
    print("[Main] Программа успешно завершена")