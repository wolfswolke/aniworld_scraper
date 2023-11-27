import logging

logging.basicConfig(level=logging.DEBUG)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger
