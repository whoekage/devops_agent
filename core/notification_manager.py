from typing import List
from .notifications import NotificationInterface

class NotificationManager:
    def __init__(self):
        self.handlers = []
        
    def notify(self, message: str, severity: str):
        """Отправка уведомления через все доступные каналы"""
        print(f"[{severity.upper()}] {message}") 