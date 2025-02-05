import logging
import ollama
from core.config import load_config
import core.tools as tools

# Настройка логирования для модуля
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class LLMClient:
    def __init__(self, api_url, model, system_prompt):
        self.api_url = api_url
        self.model = model
        self.system_prompt = system_prompt

    def analyze(self, data, agent_prompt):
        """
        Отправляет данные в LLM через Ollama (без использования инструментов).
        """
        prompt = f"{self.system_prompt}\n\n{agent_prompt}\n\nДанные:\n{data}"
        logger.debug(f"Отправляем prompt: {prompt}")
        try:
            result = ollama.generate(self.model, prompt, stream=False)
            if hasattr(result, "error") and result.error:
                logger.error(f"[LLM] Ошибка API: {result.error}")
                return f"Ошибка API: {result.error}"
            if hasattr(result, "response") and result.response:
                logger.debug(f"[LLM] Получен ответ: {result.response[:200]}...")  # выводим начало ответа
                return result.response
            else:
                logger.error("[LLM] В ответе отсутствует поле 'response'")
                return "Ошибка анализа: неверный формат ответа"
        except Exception as e:
            logger.exception("Ошибка отправки запроса в LLM")
            return f"Ошибка отправки в LLM: {str(e)}"

class LLMProcessor:
    def __init__(self):
        self.config = load_config()
        self.model = self.config["llm"]["model"]
        self.api_url = self.config["llm"]["api_url"]
        self.system_prompt = self.config["llm"]["system_prompt"]
        
    def process(self, prompt: str) -> str:
        """
        Отправляет запрос к LLM через Ollama с инструментами и получает ответ.
        Инструменты (tools) передаются как функции:
            - view_pod_logs
            - add_two_numbers

        Ollama с поддержкой tool calling сгенерирует в ответе поле tool_calls,
        которое затем используется для вызова соответствующих функций.
        """
        try:
            logger.debug(f"Отправляем запрос LLM с prompt: {prompt}")
            response = ollama.chat(
                self.model,
                messages=[{'role': 'user', 'content': prompt}],
                tools=[tools.view_pod_logs, tools.add_two_numbers]
            )
            logger.debug(f"Получен полный ответ от LLM: {response}")
            content = response.message.content

            available_functions = {
                "view_pod_logs": tools.view_pod_logs,
                "add_two_numbers": tools.add_two_numbers,
            }
            tool_outputs = []
            # Обработка вызовов инструментов из ответа LLM
            for tool_call in response.message.tool_calls or []:
                logger.debug(f"Обработка вызова функции: {tool_call.function.name} с аргументами: {tool_call.function.arguments}")
                function_to_call = available_functions.get(tool_call.function.name)
                if function_to_call:
                    result = function_to_call(**tool_call.function.arguments)
                    logger.debug(f"Результат выполнения функции {tool_call.function.name}: {result}")
                    tool_outputs.append(f"Output from {tool_call.function.name}: {result}")
                else:
                    logger.error(f"Функция {tool_call.function.name} не найдена.")
                    tool_outputs.append(f"Function not found: {tool_call.function.name}")
            if tool_outputs:
                content += "\n\n[Tool Outputs]\n" + "\n".join(tool_outputs)
            logger.debug(f"Итоговый контент: {content}")
            return content
        except Exception as e:
            logger.exception("Ошибка при обработке запроса LLM")
            return "Ошибка анализа"
