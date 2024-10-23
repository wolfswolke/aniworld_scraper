import os
from src.custom_logging import setup_logger
from datetime import datetime, timezone 

utcTime = datetime.now(timezone.utc)

logger = setup_logger(__name__)
failureFilepath = "logs/failures.log"
if not os.path.exists("logs"):
    os.mkdir("logs")
if not os.path.isfile(failureFilepath):
    open(failureFilepath, "w").close()    
failures = []

logger.info(f"Loading failure from {failureFilepath}")
writer = open(failureFilepath, "r")
lines = writer.readlines()
writer.close()
for line in lines:
    fail = line.strip('\n')
    failures.append(fail)

def remove_failure(failure):
    for fail in failures:
        if fail.find(failure) != -1:
            logger.info(f"Removing failure from file {failure}")
            failures.remove(fail)
            writer = open(failureFilepath, "r")
            lines = writer.readlines()
            writer.close()
            writer = open(failureFilepath, "w") 
            for line in lines:
                if line.find(failure) == -1:
                    writer.write(line)
            writer.close()

def append_failure(failure, url):
    logger.info(f"Appended failure {failure}")
    completeFailure = f"[{utcTime.astimezone().isoformat()}] {failure} - {url}"
    # append failure if not already in list
    for fail in failures:
        if fail.find(failure) != -1:
            return   
    
    writer = open(failureFilepath, "a")
    writer.write(completeFailure)
    writer.write("\n")
    writer.close()
    failures.append(completeFailure)

def write_fails():
    logger.debug("Writing failures")
    failures.sort()
    writer = open(failureFilepath, "w")
    for failure in failures:
        writer.write(failure)
        writer.write("\n")
    writer.close()

def remove_file(fileName):
    logger.debug("Removing {path}")
    if os.path.isfile(fileName):
        os.remove(fileName)
        logger.info(f"Removed {fileName}")
    else:
        logger.error(f"Could not remove {fileName}")

def remove_path(path):
    logger.debug("Removing {path}")
    if os.path.exits(path):
        os.remove(path)
        logger.info(f"Removed {path}")
    else:
        logger.error(f"Could not remove {path}")