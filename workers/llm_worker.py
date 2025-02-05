import zmq
import json
from core.llm import LLMClient, LLMProcessor
from core.database import Database
from core.config import load_config

def start_llm_worker(running_check=lambda: True):
    """Запуск обработчика LLM"""
    config = load_config()
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect(config["zeromq"]["host"])

    db = Database(config["sqlite"]["db_path"])
    llm = LLMProcessor()
    # Получаем промпт для k8s агента
    k8s_prompt = next((a["llm_prompt"] for a in config["agents"] if a["name"] == "k8s_agent"), "")

    print("[LLM Worker] Ожидание событий...")
    
    # Устанавливаем таймаут для recv, чтобы можно было проверять флаг running
    socket.setsockopt(zmq.RCVTIMEO, 1000)  # таймаут 1 секунда

    while running_check():
        try:
            message = socket.recv_json()
            
            if message.get("agent") == "k8s_agent":
                prompt = ""
                
                if message["type"] == "events":
                    prompt = f"{k8s_prompt}\nEvent data:\n{message}"
                elif message["type"] == "pods_status":
                    prompt = f"{k8s_prompt}\nPods status data:\n{message}"
                elif message["type"] == "nodes_usage":
                    prompt = f"{k8s_prompt}\nNodes usage data:\n{message}"
                    
                if prompt:
                    analysis = llm.process(prompt)
                    cleaned_analysis = analysis.split("</think>")[-1].strip() if "</think>" in analysis else analysis
                    print(f"\n[LLM] Analysis: {cleaned_analysis}")
                    db.insert_event(message, analysis)
        except zmq.error.Again:
            # Таймаут recv - это нормально, продолжаем цикл
            continue
        except Exception as e:
            print(f"[LLM Worker] Ошибка: {str(e)}")
            
    print("[LLM Worker] Завершение работы...")
    socket.close()
    context.term()

if __name__ == "__main__":
    start_llm_worker()
