"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
import os
import time
import sys

from logic.search_for_links import find_cache_url, get_redirect_link_by_provider
from logic.collect_all_seasons_and_episodes import get_season
from logic.collect_all_seasons_and_episodes import get_episodes
from logic.downloader import create_new_download_thread, already_downloaded
from logic.language import LanguageError
from zk_tools.logging_handle import logger

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
APP_VERSION = "v01-09-00"
MODULE_LOGGER_HEAD = "start_app.py -> "

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #
name = "Name-Goes-Here"
type = "anime" # choose 'serie' or 'anime'
language = "Deutsch"
season_override = 0  # 0 = no override. 1 = season 1. etc...
ddos_protection_calc = 5
ddos_wait_timer = 60
output_path = name

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #


def setup_logging(logging_level):
    logger.set_logging_level(logging_level)
    logger.set_cmd_line_logging_output()
    logger.add_global_except_hook()


def setup_arguments(site_url, url):
    if len(sys.argv) < 4:
        logger.info(MODULE_LOGGER_HEAD + "Usage: start_app.py <TYPE> <NAME> <LANGUAGE> [SeasonOverride]")
        sys.exit()

    global type
    type = sys.argv[1]

    global name
    name = sys.argv[2]

    global language
    language = sys.argv[3]

    url = "{}/{}/stream/{}/".format(site_url[type], type, name)

    global output_path
    output_path = name

    if len(sys.argv) == 5:
        global season_override
        season_override = int(sys.argv[4])
        logger.debug(MODULE_LOGGER_HEAD + "Season Override detected. Val: {}".format(season_override))
    else:
        logger.debug(MODULE_LOGGER_HEAD + "No Season Override.")

    return url
# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #


def main(ddos_start_value, ddos_protection_calc, ddos_wait_timer, site_url, url):
    setup_logging("info")
    if name == "Name-Goes-Here":
        url = setup_arguments(site_url, url)

    logger.info("------------- AnimeSerienScraper {} started ------------".format(APP_VERSION))

    read_check = os.access('DO_NOT_DELETE.txt', os.R_OK)
    if read_check:
        logger.debug(MODULE_LOGGER_HEAD + "We have Read Permission")
    else:
        logger.error(MODULE_LOGGER_HEAD + "No Read Permission. Please check if you own the Folder and/or have "
                                            "permissions to read.")
        exit()
    write_check = os.access('DO_NOT_DELETE.txt', os.W_OK)
    if write_check:
        logger.debug(MODULE_LOGGER_HEAD + "We have Write Permission")
    else:
        logger.error(MODULE_LOGGER_HEAD + "No Write Permission. Please check if you own the Folder and/or have "
                                            "permissions to write.")
        exit()

    if name == "Name-Goes-Here":
        logger.error(MODULE_LOGGER_HEAD + "Name is Default. Please reade readme before starting.")
        exit()

    if season_override == 0:
        logger.info(MODULE_LOGGER_HEAD + "No Season override detected.")
        seasons = get_season(url)
        logger.info(MODULE_LOGGER_HEAD + "We have this many seasons: {}".format(seasons))
    else:
        logger.info(MODULE_LOGGER_HEAD + "Season Override detected. Override set to: {}".format(season_override))
        seasons = 1

    os.makedirs(output_path, exist_ok=True)

    for season in range(int(seasons)):
        season = season + 1 if season_override == 0 else season_override
        season_path = f"{output_path}/Season {season:02}"
        os.makedirs(season_path, exist_ok=True)
        episode_count = get_episodes(url, season)
        logger.info(MODULE_LOGGER_HEAD + "Season {} has {} Episodes.".format(season, episode_count))

        for episode in range(int(episode_count)):
            episode = episode + 1
            file_name = "{}/{} - s{:02}e{:02} - {}.mp4".format(season_path, name, season, episode, language)
            logger.info(MODULE_LOGGER_HEAD + "File name will be: " + file_name)
            if not already_downloaded(file_name):
                link = url + "staffel-{}/episode-{}".format(season, episode)
                try:
                    redirect_link, provider = get_redirect_link_by_provider(site_url[type], link, language)
                except LanguageError:
                    continue
                if ddos_start_value < ddos_protection_calc:
                    logger.debug(MODULE_LOGGER_HEAD + "Entered DDOS var check and starting new downloader.")
                    ddos_start_value += 1
                else:
                    logger.info(MODULE_LOGGER_HEAD + "Started {} Downloads. Waiting for {} Seconds to not trigger DDOS"
                                                    "Protection.".format(ddos_protection_calc, ddos_wait_timer))
                    time.sleep(ddos_wait_timer)
                    ddos_start_value = 1
                cache_url = find_cache_url(redirect_link, provider)
                if cache_url == 0:
                    logger.error(MODULE_LOGGER_HEAD + f"Could not find cache url for {provider} on {season}, {episode}.")
                    continue
                logger.debug(MODULE_LOGGER_HEAD + "{} Cache URL is: ".format(provider) + cache_url)
                create_new_download_thread(cache_url, file_name, provider)


if __name__ == "__main__":
    site_url = {"serie": "https://s.to", # maybe you need another dns to be able to use this site
                "anime": "https://aniworld.to"}
    url = "{}/{}/stream/{}/".format(site_url[type], type, name)

    try:
        main(0, ddos_protection_calc, ddos_wait_timer, site_url, url)

    # except Exception as e:
    #     logger.error(MODULE_LOGGER_HEAD + "----------")
    #     logger.error(MODULE_LOGGER_HEAD + f"Exception: {e}")
    #     logger.error(MODULE_LOGGER_HEAD + "----------")

    except KeyboardInterrupt:
        logger.info("-----------------------------------------------------------")
        logger.info("            AnimeSerienScraper Stopped")
        logger.info("-----------------------------------------------------------")
        logger.info("Downloads may still be running. Please dont close this Window until its done.")
        logger.info(
            "You will know its done once you see your primary prompt string. Example: C:\\XXX or username@hostname:")
