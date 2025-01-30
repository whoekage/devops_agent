from abc import ABC, abstractmethod

class NotificationInterface(ABC):
    @abstractmethod
    async def send(self, message: str):
        pass

class SlackNotification(NotificationInterface):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        
    async def send(self, message: str):
        # Отправка уведомления в Slack
        pass

class EmailNotification(NotificationInterface):
    def __init__(self, config: dict):
        self.smtp_config = config
        
    async def send(self, message: str):
        # Отправка email уведомления
        pass 