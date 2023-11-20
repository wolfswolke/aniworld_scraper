"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
import os
import time
import sys

from .logic.search_for_links import find_cache_url, get_redirect_link_by_provider
from .logic.collect_all_seasons_and_episodes import get_season
from .logic.collect_all_seasons_and_episodes import get_episodes
from .logic.downloader import create_new_download_thread, already_downloaded
from .logic.language import LanguageError
import logging
from .constants import APP_VERSION, name, type_of_media, name, language, output_path, season_override


MODULE_LOGGER_HEAD = "start_app.py -> "


# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #

def setup_arguments(site_url):
    if len(sys.argv) < 4:
        logging.info(MODULE_LOGGER_HEAD + "Usage: start_app.py <TYPE> <NAME> <LANGUAGE> [SeasonOverride]")
        sys.exit()

    global type_of_media
    type_of_media = sys.argv[1]

    global name
    name = sys.argv[2]

    global language
    language = sys.argv[3]

    url = "{}/{}/stream/{}/".format(site_url[type_of_media], type_of_media, name)

    global output_path
    output_path = name

    if len(sys.argv) == 5:
        global season_override
        season_override = int(sys.argv[4])
        logging.debug(MODULE_LOGGER_HEAD + "Season Override detected. Val: {}".format(season_override))
    else:
        logging.debug(MODULE_LOGGER_HEAD + "No Season Override.")

    return url
# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #


def main(ddos_start_value, ddos_protection_calc, ddos_wait_timer, site_url, url):
    if name == "Name-Goes-Here":
        url = setup_arguments(site_url, url)

    logging.info("------------- AnimeSerienScraper {} started ------------".format(APP_VERSION))

    read_check = os.access('DO_NOT_DELETE.txt', os.R_OK)
    if read_check:
        logging.debug(MODULE_LOGGER_HEAD + "We have Read Permission")
    else:
        logging.error(MODULE_LOGGER_HEAD + "No Read Permission. Please check if you own the Folder and/or have "
                                            "permissions to read.")
        exit()
    write_check = os.access('DO_NOT_DELETE.txt', os.W_OK)
    if write_check:
        logging.debug(MODULE_LOGGER_HEAD + "We have Write Permission")
    else:
        logging.error(MODULE_LOGGER_HEAD + "No Write Permission. Please check if you own the Folder and/or have "
                                            "permissions to write.")
        exit()

    if name == "Name-Goes-Here":
        logging.error(MODULE_LOGGER_HEAD + "Name is Default. Please reade readme before starting.")
        exit()

    if season_override == 0:
        logging.info(MODULE_LOGGER_HEAD + "No Season override detected.")
        seasons = get_season(url)
        logging.info(MODULE_LOGGER_HEAD + "We have this many seasons: {}".format(seasons))
    else:
        logging.info(MODULE_LOGGER_HEAD + "Season Override detected. Override set to: {}".format(season_override))
        seasons = 1

    os.makedirs(output_path, exist_ok=True)

    for season in range(int(seasons)):
        season = season + 1 if season_override == 0 else season_override
        season_path = f"{output_path}/Season {season:02}"
        os.makedirs(season_path, exist_ok=True)
        episode_count = get_episodes(url, season)
        logging.info(MODULE_LOGGER_HEAD + "Season {} has {} Episodes.".format(season, episode_count))

        for episode in range(int(episode_count)):
            episode = episode + 1
            file_name = "{}/{} - s{:02}e{:02} - {}.mp4".format(season_path, name, season, episode, language)
            logging.info(MODULE_LOGGER_HEAD + "File name will be: " + file_name)
            if not already_downloaded(file_name):
                link = url + "staffel-{}/episode-{}".format(season, episode)
                try:
                    redirect_link, provider = get_redirect_link_by_provider(site_url[type_of_media], link, language)
                except LanguageError:
                    continue
                if ddos_start_value < ddos_protection_calc:
                    logging.debug(MODULE_LOGGER_HEAD + "Entered DDOS var check and starting new downloader.")
                    ddos_start_value += 1
                else:
                    logging.info(MODULE_LOGGER_HEAD + "Started {} Downloads. Waiting for {} Seconds to not trigger DDOS"
                                                    "Protection.".format(ddos_protection_calc, ddos_wait_timer))
                    time.sleep(ddos_wait_timer)
                    ddos_start_value = 1
                cache_url = find_cache_url(redirect_link, provider)
                if cache_url == 0:
                    logging.error(MODULE_LOGGER_HEAD + f"Could not find cache url for {provider} on {season}, {episode}.")
                    continue
                logging.debug(MODULE_LOGGER_HEAD + "{} Cache URL is: ".format(provider) + cache_url)
                create_new_download_thread(cache_url, file_name, provider)

