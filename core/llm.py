import requests
from core.config import load_config

class LLMClient:
    def __init__(self, api_url, model, system_prompt):
        self.api_url = api_url
        self.model = model
        self.system_prompt = system_prompt

    def analyze(self, data, agent_prompt):
        """Отправляет данные в LLM"""
        prompt = f"{self.system_prompt}\n\n{agent_prompt}\n\nДанные:\n{data}"
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        
        try:
            response = requests.post(self.api_url, json=payload)
            return response.json().get("text", "Ошибка анализа")
        except Exception as e:
            return f"Ошибка отправки в LLM: {str(e)}"

class LLMProcessor:
    def __init__(self):
        self.config = load_config()
        self.model = self.config["llm"]["model"]
        self.api_url = self.config["llm"]["api_url"]
        self.system_prompt = self.config["llm"]["system_prompt"]
        
    def process(self, prompt: str) -> str:
        """Отправляет запрос к LLM и получает ответ"""
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": self.system_prompt,
                    "stream": False
                }
            )
            return response.json()["response"]
        except Exception as e:
            print(f"[LLM] Ошибка при обработке запроса: {str(e)}")
            return "Ошибка анализа"
