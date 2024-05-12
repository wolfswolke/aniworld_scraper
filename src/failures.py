import os
from src.custom_logging import setup_logger

logger = setup_logger(__name__)
filename = "logs/failures.log"
open(filename, "w").close()
failures = []


def append_failure(failure):
    logger.info(f"Appended failure {failure}")
    writer = open(filename, "a")
    writer.write(failure)
    writer.write("\n")
    writer.close()
    failures.append(failure)


def write_fails():
    logger.debug("Writing failures")
    failures.sort()
    writer = open(filename, "w")
    for failure in failures:
        writer.write(failure)
        writer.write("\n")
    writer.close()


def remove_file(path):
    logger.debug("Removing {path}")
    if os.path.exists(path):
        os.remove(path)
        logger.info(f"Removed {path}")
    else:
        logger.error(f"Could not remove {path}")
