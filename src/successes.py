import os
import time

from src.custom_logging import setup_logger

logger = setup_logger(__name__)
filename = "logs/successes.log"
if not os.path.exists("logs"):
    os.mkdir("logs")
if not os.path.exists(filename):
    open(filename, "w").close()
# open(filename, "w").close()
successes = []


def append_success(success):
    logger.debug(f"Appended success {success}")
    writer = open(filename, "a")
    writer.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {success}")
    writer.write("\n")
    writer.close()
    successes.append(success)


def write_success():
    logger.debug("Writing successes")
    successes.sort()
    if os.path.exists(filename):
        i = 1
        while os.path.exists(f"{filename}_old_{i}"):
            i += 1
        os.rename(filename, f"{filename}_old_{i}")
    # if older then 40, remove the oldest and rename the rest
    if len(successes) > 40:
        os.remove(f"{filename}_old_{i-40}")
        for j in range(i-39, i):
            os.rename(f"{filename}_old_{j}", f"{filename}_old_{j-1}")
    writer = open(filename, "w")
    for success in successes:
        writer.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {success}")
        writer.write("\n")
    writer.close()
