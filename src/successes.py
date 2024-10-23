import os
from src.custom_logging import setup_logger
from src.failures import remove_failure
from datetime import datetime, timezone 

logger = setup_logger(__name__)
successFilepath = "logs/successes.log"
if not os.path.exists("logs"):
    os.mkdir("logs")
if not os.path.isfile(successFilepath):
    open(successFilepath, "w").close()
successes = []

logger.info(f"Loading successes from {successFilepath}")
writer = open(successFilepath, "r")
lines = writer.readlines()
writer.close()
for line in lines:
    successes.append(line.strip("\n"))

def check_real_file_exists(file_name):
    if os.path.isfile(file_name) and os.path.getsize(file_name) > 0:
        logger.info("Episode {} already downloaded.".format(file_name))
        return True
    logger.debug("File not downloaded. Downloading: {}".format(file_name))
    return False

def check_file_downloaded_before(file_name):
    if file_name in successes:
        logger.info(f"File {file_name} was already downloaded before.")
        return True
    check = check_real_file_exists(file_name)
    if check:
        append_success(file_name)
        return True
    return False

def append_success(success):
    logger.debug(f"Appended success {success}")
    utcTime = datetime.now(timezone.utc)
    completeSuccess = f"[{utcTime.astimezone().isoformat()}] {success}"
    remove_failure(success)
    # append success if not already in list
    for line in successes:
        if line.find(success) != -1:
            return   
    
    writer = open(successFilepath, "a")
    writer.write(completeSuccess)
    writer.write("\n")
    writer.close()
    successes.append(completeSuccess)

def write_succs():
    logger.debug("Writing successes")
    successes.sort()
    writer = open(successFilepath, "w")
    for success in successes:
        writer.write(success)
        writer.write("\n")
    writer.close()

def append_write_succs():
    logger.debug("Append writing successes")
    successes.sort()
    writer = open(successFilepath, "a")
    for success in successes:
        writer.write(success)
        writer.write("\n")
    writer.close()