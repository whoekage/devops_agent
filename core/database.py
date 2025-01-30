import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self._setup()

    def _setup(self):
        """Создаёт таблицу, если её нет"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    type TEXT,
                    message TEXT,
                    reason TEXT,
                    source TEXT,
                    llm_analysis TEXT
                )
            """)
            conn.commit()

    def insert_event(self, event_data, llm_result):
        """Сохраняет событие в SQLite"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO events (timestamp, type, message, reason, source, llm_analysis)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                event_data.get("timestamp"),
                event_data.get("type"),
                event_data.get("message"),
                event_data.get("reason"),
                event_data.get("source"),
                llm_result
            ))
            conn.commit()
