import os
from src.custom_logging import setup_logger
import time

logger = setup_logger(__name__)
filename = "logs/failures.log"
#open(filename, "w").close()
if not os.path.exists("logs"):
    os.mkdir("logs")
if not os.path.exists(filename):
    open(filename, "w").close()
failures = []


def append_failure(failure):
    logger.info(f"Appended failure {failure}")
    writer = open(filename, "a")
    writer.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {failure}")
    writer.write("\n")
    writer.close()
    failures.append(failure)


def write_fails():
    logger.debug("Writing failures")
    failures.sort()
    if os.path.exists(filename):
        i = 1
        while os.path.exists(f"{filename}_old_{i}"):
            i += 1
        os.rename(filename, f"{filename}_old_{i}")
    if len(failures) > 40:
        os.remove(f"{filename}_old_{i-40}")
        for j in range(i-39, i):
            os.rename(f"{filename}_old_{j}", f"{filename}_old_{j-1}")
    writer = open(filename, "w")
    for failure in failures:
        writer.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {failure}")
        writer.write("\n")
    writer.close()


def remove_file(path):
    logger.debug(f"Removing {path}")
    if os.path.exists(path):
        os.remove(path)
        logger.info(f"Removed {path}")
    else:
        logger.error(f"Could not remove {path}")
