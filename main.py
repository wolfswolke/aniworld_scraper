from src.start_app import main
import logging
from src.constants import name, ddos_protection_calc, ddos_wait_timer, type_of_media

logging.basicConfig(level=logging.DEBUG)

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #
if __name__ == "__main__":
    site_url = {"serie": "https://s.to",  # maybe you need another dns to be able to use this site
                "anime": "https://aniworld.to"}
    url = "{}/{}/stream/{}/".format(site_url[type_of_media], type_of_media, name)

    try:
        main(0, ddos_protection_calc, ddos_wait_timer, site_url, url)

    # except Exception as e:
    #     logging.error(MODULE_LOGGER_HEAD + "----------")
    #     logging.error(MODULE_LOGGER_HEAD + f"Exception: {e}")
    #     logging.error(MODULE_LOGGER_HEAD + "----------")

    except KeyboardInterrupt:
        logging.info("-----------------------------------------------------------")
        logging.info("            AnimeSerienScraper Stopped")
        logging.info("-----------------------------------------------------------")
        logging.info("Downloads may still be running. Please dont close this Window until its done.")
        logging.info(
            "You will know its done once you see your primary prompt string. Example: C:\\XXX or username@hostname:")