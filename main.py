from src.start_app import main
import logging

logging.basicConfig(level=logging.DEBUG)

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #
if __name__ == "__main__":
    try:
        main()



    except KeyboardInterrupt:
        logging.info("-----------------------------------------------------------")
        logging.info("            AnimeSerienScraper Stopped")
        logging.info("-----------------------------------------------------------")
        logging.info("Downloads may still be running. Please dont close this Window until its done.")
        logging.info(
            "You will know its done once you see your primary prompt string. Example: C:\\XXX or username@hostname:")

    except Exception as e:
        logging.error("----------")
        logging.error(f"Exception: {e}")
        logging.error("----------")