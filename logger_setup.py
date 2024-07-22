# logger_setup.py

import logging
import logging.handlers
import sys

def setup_logger(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s %(process)d:%(thread)d %(name)s %(levelname)-8s %(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.NOTSET)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024**2, backupCount=1)
    file_handler.setLevel(logging.NOTSET)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
