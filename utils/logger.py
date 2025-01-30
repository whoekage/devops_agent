import logging
from pathlib import Path

def setup_logger(config: dict):
    """Настройка логирования"""
    log_path = Path(config['file'])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=config['level'],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config['file']),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__) 