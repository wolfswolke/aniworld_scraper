from src.custom_logging import setup_logger

logger = setup_logger(__name__)
filename = "logs/successes.log"
open(filename, "w").close()
successes = []


def append_success(success):
    logger.debug(f"Appended success {success}")
    writer = open(filename, "a")
    writer.write(success)
    writer.write("\n")
    writer.close()
    successes.append(success)


def write_succs():
    logger.debug("Writing successes")
    successes.sort()
    writer = open(filename, "w")
    for success in successes:
        writer.write(success)
        writer.write("\n")
    writer.close()
