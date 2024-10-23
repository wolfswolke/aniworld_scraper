import logging
import os

LOADING = 24
SUCCESS = 25
logging.addLevelName(LOADING, "LOADING")
logging.addLevelName(SUCCESS, "SUCCESS")


if not os.path.exists("logs"):
    os.mkdir("logs")

def loading(self, message, *args, **kwargs):
    if self.isEnabledFor(LOADING):
        self._log(LOADING, message, args, **kwargs)

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)


logging.Logger.loading = loading
logging.Logger.success = success

logging.basicConfig(level=logging.INFO)


class CustomFormatter(logging.Formatter):
    green = "\033[1;92m"
    yellow = "\033[1;93m"
    red = "\033[1;31m"
    purple = "\033[1;35m"
    blue = "\033[1;94m"
    reset = "\033[0m"
    format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s "

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: red + format + reset,
        LOADING: purple + format + reset,
        SUCCESS: green + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    # Prevent passing events to the handlers of higher severity
    logger.propagate = False
    # Set formatter for the logger.
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    return logger
