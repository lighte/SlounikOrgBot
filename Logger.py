# logger.py
import logging
from logging.handlers import RotatingFileHandler

MAX_FILE_SIZE_MB = 1
MAX_FILE_COUNT = 10
LOG_RECORD_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOGGERS = {}

def get_logger(name='my_app', log_file='app.log'):
    if not name in LOGGERS:
        new_logger(name, log_file)
    return LOGGERS[name]

def new_logger(name, log_file):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = RotatingFileHandler(log_file,
            maxBytes = MAX_FILE_SIZE_MB * 1024 * 1024,
            backupCount = MAX_FILE_COUNT)
        formatter = logging.Formatter(LOG_RECORD_FORMAT)
        handler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    LOGGERS[name] = logger