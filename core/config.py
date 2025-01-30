import yaml
from pathlib import Path

def load_config(config_path: str = "config.yaml") -> dict:
    """Загрузка конфигурации из YAML файла"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)