from src.custom_logging import setup_logger
from src.start_app import main

logger = setup_logger(__name__)

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #
if __name__ == "__main__":
    try:
        main()



    except KeyboardInterrupt:
        logger.info("-----------------------------------------------------------")
        logger.info("            AnimeSerienScraper Stopped")
        logger.info("-----------------------------------------------------------")
        logger.info("Downloads may still be running. Please don't close this Window until its done.")
        logger.info(
            "You will know its done once you see your primary prompt string. Example: C:\\XXX or username@hostname:")

    except Exception as e:
        logger.error("----------")
        logger.error(f"Exception: {e}")
        logger.error("----------")
