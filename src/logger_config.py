import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_logger(module_name):
    project_root = Path(__file__).resolve().parent.parent
    log_path = project_root / 'logs'
    log_path.mkdir(exist_ok=True)
    
    log_file = log_path / 'pipeline.log'

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=4)
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger